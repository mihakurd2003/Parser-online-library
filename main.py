import requests
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    if not os.path.exists('books'):
        os.makedirs('books', exist_ok=True)

    for id in range(32168, 32178):
        response = requests.get(url=f'https://tululu.org/txt.php?id={id}', verify=False)
        response.raise_for_status()

        with open(f'books/id{id}.txt', 'w', encoding='utf-8') as file:
            file.write(response.text)


if __name__ == '__main__':
    main()

