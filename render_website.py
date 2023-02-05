from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from urllib.parse import urlsplit


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open('books.json', 'r', encoding='UTF-8') as file:
        books = json.loads(file.read())

    for book in books:
        book['image_url'] = urlsplit(book['image_url']).path.split('/')[-1]

    rendered_page = template.render(
        books=books,
    )

    with open('index.html', 'w', encoding="utf-8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()