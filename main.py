import requests
import urllib3
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit
from argparse import ArgumentParser

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def parse_book_page(html_content):
    soup = BeautifulSoup(html_content, 'lxml')

    title, author = list(map(lambda el: el.strip(), soup.find('div', {'id': 'content'}).find('h1').text.split('::')))
    image_url = urljoin('https://tululu.org', soup.find('div', {'id': 'content'}).find('div', {'class': 'bookimage'}).find('img').get('src'))
    text = soup.find('div', {'id': 'content'}).find_all('table', {'class': 'd_book'})[-1].text.strip()
    comment = list(map(lambda el: el.find('span', {'class': 'black'}).text.strip(), soup.find('div', {'id': 'content'}).find_all('div', {'class': 'texts'})))
    genre = list(map(lambda el: el.text.strip(), soup.find('div', {'id': 'content'}).find('span', {'class': 'd_book'}).find_all('a')))

    return {
        'title': title,
        'author': author,
        'image_url': image_url,
        'text': text,
        'comment': comment,
        'genre': genre,
    }


def download_txt(url, filename, folder='books/'):
    os.makedirs(folder, exist_ok=True)

    upd_filename = sanitize_filename(filename)
    response = requests.get(url=url)
    response.raise_for_status()
    check_for_redirect(response)

    with open(f'{folder}{upd_filename}.txt', 'w', encoding='utf-8') as file:
        file.write(response.text)

    return os.path.join(folder, upd_filename)


def download_image(url, folder='images/'):
    os.makedirs(folder, exist_ok=True)

    filename = urlsplit(url).path.split('/')[-1]
    response = requests.get(url=url)
    response.raise_for_status()

    with open(f'{folder}{filename}', 'wb') as file:
        file.write(response.content)


def main():
    url = 'https://tululu.org'
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--start_id', type=int, default=0)
    arg_parser.add_argument('--end_id', type=int)
    args = arg_parser.parse_args()
    if not args.end_id:
        args.end_id = args.start_id + 10

    for id in range(args.start_id, args.end_id):
        try:
            response = requests.get(url=urljoin(url, f'b{id}/'))
            response.raise_for_status()
            check_for_redirect(response)

            parsed_book = parse_book_page(response.text)

            download_txt(url=urljoin(url, f'/txt.php?id={id}'), filename=parsed_book['title'])
            download_image(parsed_book['image_url'])

        except requests.exceptions.HTTPError:
            print(f'HTTP_error or redirect on id = {id}')


if __name__ == '__main__':
    main()
