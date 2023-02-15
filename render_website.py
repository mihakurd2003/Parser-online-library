import json
import os
import re
from argparse import ArgumentParser
from urllib.parse import urlsplit

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def parse_argument(argument):
    arg_parser = ArgumentParser(description='Позволяет указать свой путь к файлу .json')
    arg_parser.add_argument(argument, default='books.json', help='Путь до файла .json')
    args = arg_parser.parse_args()

    return args


def rebuild_page():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    args = parse_argument('--path')

    with open(args.path, 'r', encoding='UTF-8') as file:
        book_cards = json.load(file)

    os.makedirs('pages', exist_ok=True)

    for book_card in book_cards:
        book_card['image_url'] = urlsplit(book_card['image_url']).path.split('/')[-1]
        book_card['url_book'] = re.sub(r'[^\w_ -]', '', book_card['title'])

    columns_count, book_cards_count = 2, 10
    chunked_book_cards = list(chunked(list(chunked(book_cards, columns_count)), book_cards_count))
    page_count = len(chunked_book_cards)

    for num_page, books_on_page in enumerate(chunked_book_cards, start=1):
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
