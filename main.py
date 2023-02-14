import sys
import time
import urllib3
import os
from urllib.parse import urljoin, urlsplit
from pathvalidate import sanitize_filename

import requests
from bs4 import BeautifulSoup
from argparse import ArgumentParser

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def parse_book_page(html_content, url):
    soup = BeautifulSoup(html_content, 'lxml')

    header_book = soup.find('div', id='content').find('h1').text
    title, author = list(map(lambda el: el.strip(), header_book.split('::')))

    image_block = soup.select_one('.bookimage img')['src']
    image_url = urljoin(url, image_block)

    text = soup.select('table.d_book')[-1].text.strip()

    comment_block = soup.select('div.texts')
    comments = [comment.select_one('span.black').text.strip() for comment in comment_block]

    genres_block = soup.select('span.d_book a')
    genres = [genre.text.strip() for genre in genres_block]

    return {
        'title': title,
        'author': author,
        'image_url': image_url,
        'text': text,
        'comments': comments,
        'genres': genres,
    }


def download_txt(url, filename, folder='media/', params=None):
    os.makedirs(folder, exist_ok=True)

    upd_filename = f'{sanitize_filename(filename)}.txt'
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    check_for_redirect(response)

    path = os.path.join(folder, upd_filename)

    with open(path, 'w', encoding='UTF-8') as file:
        file.write(response.text)

    return path


def download_image(url, folder='media/'):
    os.makedirs(folder, exist_ok=True)

    filename = urlsplit(url).path.split('/')[-1]
    response = requests.get(url=url)
    response.raise_for_status()

    with open(f'{folder}{filename}', 'wb') as file:
        file.write(response.content)


def main():
    url = 'https://tululu.org'
    arg_parser = ArgumentParser(description='Получает множество id, промежуток которого задаёт пользователь')
    arg_parser.add_argument('--start_id', type=int, default=0, help='С этого id начинается скачивание книг')
    arg_parser.add_argument('--end_id', type=int, help='До этого id скачиваются книги')
    args = arg_parser.parse_args()
    if not args.end_id:
        args.end_id = args.start_id + 10

    for book_id in range(args.start_id, args.end_id):
        url_book = urljoin(url, f'b{book_id}/')
        payload = {'id': book_id}
        try:
            response = requests.get(url=url_book)
            response.raise_for_status()
            check_for_redirect(response)

            parsed_book = parse_book_page(response.text, url_book)

            download_txt(url=urljoin(url, '/txt.php'), params=payload, filename=parsed_book['title'])
            download_image(parsed_book['image_url'])

        except requests.exceptions.HTTPError:
            print(f'HTTP_error or redirect on id = {book_id}', file=sys.stderr)

        except requests.exceptions.ConnectionError as connection_error:
            print(str(connection_error), file=sys.stderr)
            time.sleep(10)


if __name__ == '__main__':
    main()
