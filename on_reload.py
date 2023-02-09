from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from urllib.parse import urlsplit
from livereload import Server
from more_itertools import chunked
import os
import re


def rebuild_page():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open('books.json', 'r', encoding='UTF-8') as file:
        books = json.loads(file.read())

    os.makedirs('pages', exist_ok=True)

    for book in books:
        book['image_url'] = urlsplit(book['image_url']).path.split('/')[-1]
        book['url_book'] = re.sub(r'[^\w_ -]', '', book['title'])

    page_elements_count = 10
    books = list(chunked(list(chunked(books, 2)), page_elements_count))
    page_count = len(books)

    for num_page, books_on_page in enumerate(books):
        rendered_page = template.render(
            books=books_on_page,
            page_count=page_count,
            curr_page_num=num_page + 1,
        )

        with open(f'pages/index{num_page + 1}.html', 'w', encoding="UTF-8") as file:
            file.write(rendered_page)


def main():
    rebuild_page()

    server = Server()

    server.watch('template.html', rebuild_page)
    server.serve(root='.')


if __name__ == '__main__':
    main()
