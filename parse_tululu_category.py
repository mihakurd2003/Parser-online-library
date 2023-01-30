import os

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import argparse
from main import parse_book_page, download_txt, download_image


def get_book_id(html_content):
    soup = BeautifulSoup(html_content, 'lxml')

    book_blocks = soup.select('table.d_book')
    urls_book = [block.find('a')['href'] for block in book_blocks]
    return urls_book


def main():
    parser = argparse.ArgumentParser(description='Получает множество номеров страниц, промежуток которого задаёт пользователь и другие необязательные параметры')
    parser.add_argument('--start_page', type=int, default=0, help='С этого номера страницы начинается скачивание книг')
    parser.add_argument('--end_page', type=int, default=701, help='До этого номера страницы(включительно) скачиваются книги')
    parser.add_argument('--dest_folder', default='', help='Путь до директории, в которой будут расположены такие папки, как "books/", "images/"')
    parser.add_argument('--json_path', default='', help=r'Путь до файла *.json; Пример для Windows: C:\Desktop\...\*.json')
    parser.add_argument('--skip_imgs', action='store_true', help='Пропускает скачивание картинок. Если указан, то пропускает скачивание')
    parser.add_argument('--skip_txt', action='store_true', help='Пропускает скачивание книг. Если указан, то пропускает скачивание')
    args = parser.parse_args()

    books = []
    for page in range(args.start_page, args.end_page + 1):
        url = f'https://tululu.org/l55/{page}/'
        try:
            response_page = requests.get(url=url)
            response_page.raise_for_status()

            for book_id in get_book_id(response_page.text):
                payload = {'id': book_id[2:-1]}
                url_book = urljoin(url, book_id)
                try:
                    response_book = requests.get(url=url_book)
                    response_book.raise_for_status()

                    parsed_book = parse_book_page(response_book.text, url_book)
                    if not args.skip_imgs:
                        download_image(parsed_book['image_url'], folder=os.path.join(args.dest_folder, 'images/'))
                    if not args.skip_txt:
                        download_txt(
                            url=urljoin(url_book, '/txt.php'),
                            params=payload,
                            filename=parsed_book['title'],
                            folder=os.path.join(args.dest_folder, 'books/')
                        )
                    books.append(parsed_book)
                except requests.exceptions.HTTPError:
                    print(f'Error in {url_book}')
                    continue

        except requests.exceptions.HTTPError as err:
            print(f'Error in {page} page')

    if args.json_path:
        with open(f'{args.json_path}', 'w', encoding='utf-8') as file:
            json.dump(books, file, indent=4, ensure_ascii=False)
        return

    with open(os.path.join(args.dest_folder, 'books.json'), 'w', encoding='utf-8') as file:
        json.dump(books, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
