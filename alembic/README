## Перечень команд Alembic:

- Инициализация Alembic:
```bash
alembic init --template async alembic
```
Параметр --template async необходимо указывать в тех случаях, когда используется асинхронное подключение к БД.

- Создание миграции:
```bash
alembic revision --autogenerate -m "комментарий к миграции"
```

- Выполнение всех неприменённых миграций:
```bash
alembic upgrade head
```

- Отмена всех миграций, которые были в проекте:
```bash
alembic downgrade base
```

- Применение всех миграций до указанной (указываем ID миграции):
```bash
alembic upgrade befcaa650c3f
```

- Откат миграций (отменить все миграции до миграции с ID 466f1da3d4b1):
```bash
alembic downgrade 466f1da3d4b1
```
В команде даунгрейда можно использовать сокращенные ID миграций.

- Посмотреть историю миграций:
```bash
alembic history
```

- Посмотреть последнюю применённую миграцию:
```bash
alembic current
```