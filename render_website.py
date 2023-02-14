import os
import re
import json
from urllib.parse import urlsplit

from livereload import Server
from more_itertools import chunked
from argparse import ArgumentParser
from jinja2 import Environment, FileSystemLoader, select_autoescape


def rebuild_page():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    arg_parser = ArgumentParser(description='Позволяет указать свой путь к файлу .json')
    arg_parser.add_argument('--path', default='books.json', help='Путь до файла .json')
    args = arg_parser.parse_args()

    with open(args.path, 'r', encoding='UTF-8') as file:
        books_info = json.load(file)

    os.makedirs('pages', exist_ok=True)

    for book_info in books_info:
        book_info['image_url'] = urlsplit(book_info['image_url']).path.split('/')[-1]
        book_info['url_book'] = re.sub(r'[^\w_ -]', '', book_info['title'])

    columns_count, page_elements_count = 2, 10
    chunked_books_info = list(chunked(list(chunked(books_info, columns_count)), page_elements_count))
    page_count = len(chunked_books_info)

    for num_page, books_on_page in enumerate(chunked_books_info, start=1):
        rendered_page = template.render(
            books=books_on_page,
            page_count=page_count,
            curr_page_num=num_page,
        )

        with open(f'pages/index{num_page}.html', 'w', encoding='UTF-8') as file:
            file.write(rendered_page)


def main():
    rebuild_page()

    server = Server()
    server.watch('template.html', rebuild_page)
    server.serve(root='.')


if __name__ == '__main__':
    main()
