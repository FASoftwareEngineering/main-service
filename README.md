# main-service

## Ресурсы проекта

- **[Требования](https://docs.google.com/spreadsheets/d/1GofXFF30oyyuv8pY4ic6NPHMvqzgblUg3MaRuwBuDck/edit#gid=760256269)**
- **[Дизайн архитектуры](https://app.diagrams.net/#G11At2G5mZ-JMfmA6tRvXmPy5N2Jv4FLdJ)**
- **[Дизайн хранилища](https://dbdiagram.io/d/6355eb304709410195c53272)**

## Структура проекта

### ./

- **configs/** - статические конфигурации приложения, связанные с процессом сборки приложения
- **deployments/** - содержит файлы связанные с развертыванием: манифесты Docker Compose, манифесты и
  настройки Kubernetes
- **docs/** - документация к проекту, дизайну и коду
- **src/** - код приложения и связанные с ним файлы миграций, зависимостей, конфигураций.
- **.env.example** - пример **.env** файла
- **.gitignore** - используется для того, чтобы определить, какие файлы не нужно добавлять в git репозиторий
- **.pre-commit-config.yaml** - файл конфигурации для git pre-commit hook
- **docker-compose.yml** - манифест Docker Compose
- **README.md** - 👈 вы сейчас здесь
- **start.sh** - скрипт для запуска docker-compose.yml

### src/

```
├── app/  # код приложения
│   ├── api/  # бизнес-логика и ресурсы
│   │   ├── employees/  # модуль с бизнес-логикой домена employees
│   │   ├── projects/  # модуль с бизнес-логикой домена projects
│   │   │   ├── __init__.py
│   │   │   ├── constants.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── services.py
│   │   │   └── views.py
│   │   ├── __init__.py  # настройка основного API роутера
│   │   ├── constants.py  # общие константы
│   │   ├── dependencies.py  # общие зависимости
│   │   ├── exceptions.py  # кастомные API исключения
│   │   ├── models.py  # общие модели
│   │   ├── schemas.py  # общие схемы
│   │   └── services.py  # общая бизнес-логика
│   ├── core/  # базовый, переиспользуемый функционал
│   │   └── db.py
│   ├── cli.py  # CLI команды
│   ├── config.py  # конфигурация приложения
│   ├── main.py  # создание, настройка и запуск FastAPI приложения
│   └── models.py  # раскрытие всех моделей для alembic
├── migrations/  # миграции alembic
├── tests/
│   ├── integration/  # интеграционные тесты
│   ├── unit/  # unit-тесты
│   └── conftest.py  # глобальные fixtures
├── .coverage
├── .env.example
├── .flake8
├── .gitignore
├── alembic.ini  # конфигурация alembic
├── Dockerfile
├── poetry.lock
├── pyproject.toml
├── requirements.dev.txt  # сгенерированный poetry файл dev- зависимостей для pip
└── requirements.txt  # сгенерированный poetry файл зависимостей для pip
```

Каждый доменный модуль (`employees, projects, ...`) может содержать:

- `views.py` - API ручки для работы с ресурсами
- `schemas.py` - схемы запросов и ответов API
- `models.py` - модели базы данных
- `services.py` - реализация бизнес-логики модуля
- _`constants.py` - специфические константы_
- _`exceptions.py` - специфические API исключения_
- _`dependencies.py` - для хранения зависимостей (если зависимостей мало, лучше хранить их в `views.py`)_

## Как начать разработку

Клонировать репозиторий:

```git
git clone https://github.com/FASoftwareEngineering/main-service.git
```

### Локальный запуск

Python>=3.10. Проверить версию python:

```
python --version
```

Создать виртуальное окружение. Если выберите имя отличное от `.venv` или `venv`, не забудьте добавить его
в `.gitignore`.

```
cd main-service/src/

python -m pip install -U pip
pip install -U virtualenv

python -m venv .venv
```

> Альтернативный способ создания вирутуального окружения - воспользоваться пользовательским интерфесом PyCharm
> при создании нового проекта.

Установить зависимости:

```
.\.venv\Scripts\activate  # активировать виртуальное окружение
pip install -r requirements.dev.txt
```

> Продвинутый способ управления зависимостями - [poetry](https://python-poetry.org/).

Создать файл `.env` и заполнить его по аналогии с `.env.example`.

Запустить [FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/) приложение:

```
uvicorn app.main:app --reload 
# или
python -m uvicorn app.main:app --reload 
```

Проверить работоспособность приложения, перейдя по ссылке `http://127.0.0.1:8000/docs` (у вас может быть
другая).

```
...
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [13520] using StatReload
...
```

### Docker

> TODO

[//]: # (Спроектировать и задокументировать дизайн API домена проектов)

[//]: # ()

[//]: # (Спроектировать и задокументировать дизайн API домена ресурсов)

## Road Map

| Статус | Этап                                        | Дата завершения |
|:------:|:--------------------------------------------|:----------------|
|   ▶    | Развитие и поддержка инфраструктуры проекта | 05.11.2022      |
|   ▶    | Дизайн и документирование API               | 28.10.2022      |
|  [ ]   | Реализация бизнес-логики                    | 03.11.2022      |
|  [ ]   | Написание интеграционных тестов             | 05.11.2022      |

## Цели и задачи

- реализовать функционал по работе с проектами (ФТ 1) [⭐⭐⭐⭐⭐]
- реализовать функционал по работе с ресурсами (ФТ 2) [⭐⭐]
- представить интерфейс в виде интеграционных тестов [⭐⭐⭐⭐]
- настроить CI/CD [⭐⭐⭐⭐]

## Общие задачи разработки

- разобраться с запуском проекта (локальный/Docker)
    - разобраться с [poetry](https://python-poetry.org/)
- изучить имеющиеся примеры в `src/app` и используемые в них инструменты (
  файл `src/pyproject.toml::tool.poetry.dependencies`)

## Команды и задачи разработки

### Задача 1

**Команда:** Гоша

**Задачи:**

- написать гайд: как запустить проект для разработки
- настроить линтеры (`flake8, wemake-python-styleguide, pylint, bandit`), форматеры (`black , isort`)
- добавить линтеры и форматеры в `Workflows GitHub Actions`
- настроить git-precommit-hook для линтеров и форматеров
- настроить git-precommit-hook для `poetry export -o requirements.txt`
- настроить запуск тестов в `Workflows GitHub Actions`
- настроить git-precommit-hook для запуска тестов
- помочь (написать гайд) всем с локальной настройкой `blackd`

### Задача 2

**Команда:** Полина, Оля, Настя

**Задача:** придумать и задокументировать интерфейс **для работы с проектами** в виде OpenAPI

**Как делать?**

Нужно определить схемы запросов и ответов, пути к ресурсам и методы их обработки и записать их в коде:
`app/api/projects`

```python
from app.core.schemas import BaseSchema
from fastapi import APIRouter, status


class ProjectBase(BaseSchema):
    code: str
    name: str
    start_date: datetime | None = None
    end_date: datetime | None = None


class ProjectRead(ProjectBase):  # схема ответа
    id: int


router = APIRouter(prefix=f"/projects", tags=["Projects"])


@router.get("/{project_id}", response_model=ProjectRead)  # схема ответа
def get_project(
        project_id: int,
):
    pass  # реализация на данном этапе не нужна

```

Подробнее в `src/app/api`

### Задача 3

**Команда:** Даша, Лиза, Рукижат

**Задача:** придумать и задокументировать интерфейс **для работы с ресурсами** в виде OpenAPI

**Как делать?** см. в [Задача 2](#задача-2)

## Правила работы

`TODO`
