from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from urllib.parse import urlsplit
from livereload import Server
from more_itertools import chunked
import re


def rebuild_page():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open('books.json', 'r', encoding='UTF-8') as file:
        books = json.loads(file.read())

    for book in books:
        book['image_url'] = urlsplit(book['image_url']).path.split('/')[-1]
        book['url_book'] = re.sub(r'[^\w_ -]', '', book['title'])

    books = list(chunked(books, 2))

    rendered_page = template.render(
        books=books,
    )

    with open('index.html', 'w', encoding="UTF-8") as file:
        file.write(rendered_page)


def main():
    rebuild_page()

    server = Server()

    server.watch('template.html', rebuild_page)
    server.serve(root='.')


if __name__ == '__main__':
    main()
