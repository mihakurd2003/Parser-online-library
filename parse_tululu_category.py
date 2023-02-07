import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import argparse
from main import parse_book_page, download_txt, download_image, check_for_redirect


def get_book_urls(html_content):
    soup = BeautifulSoup(html_content, 'lxml')

    book_blocks = soup.select('table.d_book')
    book_urls = [block.find('a')['href'] for block in book_blocks]
    return book_urls


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
            page_response = requests.get(url=url)
            page_response.raise_for_status()
            check_for_redirect(page_response)

            book_urls = get_book_urls(page_response.text)
            for book_address in book_urls:
                payload = {'id': book_address[2:-1]}
                book_url = urljoin(url, book_address)
                try:
                    book_response = requests.get(url=book_url)
                    book_response.raise_for_status()
                    check_for_redirect(book_response)

                    parsed_book = parse_book_page(book_response.text, book_url)
                    if not args.skip_imgs:
                        download_image(parsed_book['image_url'], folder=os.path.join(args.dest_folder, 'images/'))
                    if not args.skip_txt:
                        download_txt(
                            url=urljoin(book_url, '/txt.php'),
                            params=payload,
                            filename=parsed_book['title'],
                            folder=os.path.join(args.dest_folder, 'books/')
                        )
                    books.append(parsed_book)
                except requests.exceptions.HTTPError:
                    print(f'HTTP Error in {book_url}', file=sys.stderr)

                except requests.exceptions.ConnectionError:
                    print(f'Connection Error in {book_url}', file=sys.stderr)
                    time.sleep(10)
                    continue

        except requests.exceptions.HTTPError:
            print(f'HTTP Error in {page} page', file=sys.stderr)

        except requests.exceptions.ConnectionError:
            print(f'Connection Error in {page} page', file=sys.stderr)
            time.sleep(10)
            continue

    path = args.json_path if args.json_path else os.path.join(args.dest_folder, 'books.json')

    with open(path, 'w', encoding='UTF-8') as file:
        json.dump(books, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
