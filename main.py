import requests
import urllib3
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def url_parse(url, params):
    response = requests.get(url=urljoin(url, f'b{params["id"]}/'))
    response.raise_for_status()
    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')

    title = soup.find('div', {'id': 'content'}).find('h1').text.split('::')[0].strip()
    image_url = urljoin(url, soup.find('div', {'id': 'content'}).find('div', {'class': 'bookimage'}).find('img').get('src'))
    text = soup.find('div', {'id': 'content'}).find_all('table', {'class': 'd_book'})[-1].text.strip()

    return title, image_url, text


def download_image(url, folder='images/'):
    os.makedirs(folder, exist_ok=True)

    filename = urlsplit(url).path.split('/')[-1]
    response = requests.get(url=url)
    response.raise_for_status()

    with open(f'{folder}{filename}', 'wb') as file:
        file.write(response.content)


def download_txt(url, filename, folder='books/'):
    os.makedirs(folder, exist_ok=True)

    upd_filename = sanitize_filename(filename)
    response = requests.get(url=url)
    response.raise_for_status()
    check_for_redirect(response)

    with open(f'{folder}{upd_filename}.txt', 'w', encoding='utf-8') as file:
        file.write(response.text)

    return os.path.join(folder, upd_filename)


def main():
    url = 'https://tululu.org'

    for id in range(1, 10):
        params = {'id': id}
        try:
            title, image_url, text = url_parse(url, params)

            # print(download_txt(url=f'{url}/txt.php?id={id}', filename=title))
            download_image(image_url)

        except requests.exceptions.HTTPError:
            print(f'HTTP_error on id = {id}')


if __name__ == '__main__':
    main()
