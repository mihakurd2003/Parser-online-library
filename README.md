# Парсер книг

Парсер книг с сайта [tululu.org](https://tululu.org)

### Как установить

- Скачайте код и поместите в виртуальное окружение
```
python3 -m venv <название окружения>
```
```
<название окружения>\Scripts\activate.bat
```
```
git clone https://github.com/mihakurd2003/space.git
```

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
### Как пользоваться файлом main.py
- В терминале набирайте команду:
```
python3 main.py --start_id <начальный id> --end_id <конечный id>
```
- Получает книги в промежутке от start_id до end_id. По умолчанию start_id равен 0, end_id равен start_id + 10
### Как пользоваться файлом parse_tululu_category.py
- В терминале набирайте команду:
```
python3 parse_tululu_category.py --start_page <начальный номер страницы> --end_page <конечный номер страницы>
```
- Скачивает книги по страницам в промежутке от start_page до end_page(включительно). По умолчанию start_page равен 0, end_page равен 701
### Дополнительные аргументы к parse_tululu_category.py
- --dest_folder: Путь до директории, в которой будут расположены такие папки, как "books/", "images/"
- --json_path: Путь до файла *.json; Пример: C:/Desktop/.../\*.json
- --skip_imgs: Пропускает скачивание картинок. Если указан, то пропускает скачивание
- --skip_txt: Пропускает скачивание книг. Если указан, то пропускает скачивание
### Как запустить сайт у себя локально

- В терминале набирайте команду:
```
python3 render_website.py
```
- Переходите по адресу [127.0.0.1](http://127.0.0.1:8000)
### Ссылка на готовый сайт: [mihakurd2003.github.io](https://mihakurd2003.github.io/Parser-online-library/pages/index1.html)