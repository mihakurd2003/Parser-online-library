import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from urllib.parse import urlsplit
from more_itertools import chunked
import re


def main():
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

    books = list(chunked(list(chunked(books, 2)), 10))

    for num_page, books_on_page in enumerate(books):
        rendered_page = template.render(
            books=books_on_page,
        )

        with open(f'pages/index{num_page+1}.html', 'w', encoding="UTF-8") as file:
            file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()