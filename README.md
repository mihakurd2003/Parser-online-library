# Парсер книг

Парсер книг с сайта tululu.org

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