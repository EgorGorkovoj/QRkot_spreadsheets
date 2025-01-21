# Приложение QRKot
Учебный проект Яндекс Практикум.
QRKot - приложение для Благотворительного фонда поддержки котиков, созданное на фреймворке FastAPI.

## Цель проекта
Отработать навыки работы с FastAPI, SQLAlchemy, pydantic, Google API.

## Технологии
- Python 3.9.13
- FastAPI 0.78.0
- Uvicorn 0.17.6
- SQLAlchemy 1.4.36
- Alembic 1.7.7
- FastAPI Users 10.0.4
- Aiogoogle 4.2.0
- Google Drive API v3
- Google Sheet API v4

## Описание проекта

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых,
на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные
с поддержкой кошачьей популяции.


### Возможности проекта:
- Cоздание благотворительных проектов;
- Cоздание и автоматическое распределение между проектами пожертвований от пользователей;
- управления пользователями.

## Документация проекта
Документация проекта доступна после запуска проекта по адресам ```/docs``` и ```/redoc```


## База данных
В проекте настроено асинхронное подключение к базе данных через SQLAlchemy ORM.
Миграции базы данных настроены через библиотеку Alembic.

## Как развернуть проект на компьютере:
1. Клонировать репозиторий c GitHub на компьютер и перейти директорию:
```bash
git clone https://github.com/EgorGorkovoj/cat_charity_fund.git
```
```bash
cd cat_charity_fund
```
2. Создать и активировать виртуальное окружение
```bash
python -m venv venv
```
* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/Scripts/activate
    ```

3. Установить зависимости из файла requirements.txt:

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```
4. Создать файл .env с переменными окружения. Например:
```
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=secretpassword
```
5. Создать базу данных
```bash
alembic upgrade head
```
или например:
```bash
alembic upgrade 47bd1
```
где 47bd1 номер начала миграции.<br>
6. Запустить приложение
```bash
uvicorn app.main:app
```

## Формирования отчета в гугл-таблицы:

### Подключение к GoogleAPI

Для работы с Google API необходимо в Google Cloud Platform создать проект с сервисным аккаунтом и подключенными Google Drive API и Google Sheets API. У проекта нужно сформировать JSON-файл с ключом доступа к сервисному аккаунту и перенести его данные в файл .env.
В .env файл также следует добавить адрес личного гугл-аккаунта для выдачи прав доступа к сформированному отчету.
Пример файла .env:
```bash
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
EMAIL=example@gmail.com
TYPE=...
PROJECT_ID=...
PRIVATE_KEY_ID=...
PRIVATE_KEY="..."
CLIENT_EMAIL=...
CLIENT_ID=...
AUTH_URI=...
TOKEN_URI=...
AUTH_PROVIDER_X509_CERT_URL=...
CLIENT_X509_CERT_URL=...
```