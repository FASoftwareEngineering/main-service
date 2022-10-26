# main-service

## Road Map

| Статус | Этап                                        | Дата начала | Дата завершения |
|:------:|:--------------------------------------------|:-----------:|:---------------:|
|   🔛   | Развитие и поддержка инфраструктуры проекта | 24.10.2022  |   05.11.2022    |
|   🔛   | Дизайн и документирование API               | 24.10.2022  |   28.10.2022    |
|   🔜   | Реализация бизнес-логики                    | 29.10.2022  |   03.11.2022    |
|   🔜   | Написание интеграционных тестов             | 03.11.2022  |   05.11.2022    |

## Ресурсы проекта

- **[Требования](https://docs.google.com/spreadsheets/d/1GofXFF30oyyuv8pY4ic6NPHMvqzgblUg3MaRuwBuDck/edit#gid=760256269)**
- **[Дизайн архитектуры](https://app.diagrams.net/#G11At2G5mZ-JMfmA6tRvXmPy5N2Jv4FLdJ)**
- **[Дизайн хранилища](https://dbdiagram.io/d/6355eb304709410195c53272)**

## Структура проекта

### ./

- `configs/` - статические конфигурации приложения, связанные с процессом сборки приложения
- `deployments/` - содержит файлы связанные с развертыванием: манифесты Docker Compose, манифесты и
  настройки Kubernetes
- `docs/` - документация к проекту, дизайну и коду
- `src/` - код приложения и связанные с ним файлы миграций, зависимостей, конфигураций.
- `.env.example` - пример `.env` файла
- `.gitignore` - используется для того, чтобы определить, какие файлы не нужно добавлять в git репозиторий
- `.pre-commit-config.yaml` - файл конфигурации для git pre-commit hook
- `docker-compose.yml` - манифест Docker Compose
- `README.md` - 👈 вы сейчас здесь
- `start.sh` - скрипт для запуска docker-compose.yml

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

- [Локальный запуск](#локальный-запуск)
- [Docker](#docker)

### Локальный запуск

Python>=3.10. Проверить версию python:

```
python --version
```

Создать виртуальное окружение. Если выберите имя отличное от `.venv` или `venv` - не забудьте добавить его в `.gitignore`.

```
cd main-service/src/

python -m pip install -U pip
pip install -U virtualenv

python -m venv .venv
```

> Альтернативный способ создания виртуального окружения - воспользоваться пользовательским интерфесом PyCharm
> при создании нового проекта.

Установить зависимости:

```
.\.venv\Scripts\activate  # активировать виртуальное окружение
pip install -r requirements.dev.txt
```

> Продвинутый способ управления зависимостями - [poetry](https://python-poetry.org/).

Создать файл `.env` в корне проекта (`main-service/.env`) и заполнить его по аналогии с `.env.example`.

Запустить [FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/) приложение:

```
uvicorn app.main:app --port 8000 --reload --env-file ../.env
```

FastAPI приложение будет доступно по адресу: http://127.0.0.1:8000

```
...
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [13520] using StatReload
...
```

### Docker

Вам необходимы 2 вещи: 
- `.env` файл в корне проекта (можно получить у [@GeorgiyDemo](https://github.com/GeorgiyDemo))
- установленный docker и docker-compose

Сама развертка решения осуществляется в папке проекта следующим образом:

```
docker-compose --env-file .env up -d
```

После чего будут развернуты необходимые контейнеры для работы решения.
Для проверки развертки можно воспользоваться командой:

```
docker ps
```
На output должны вывестись N контейнеров

FastAPI приложение будет доступно по адресу: http://127.0.0.1:80

### Команды, используемые в разработке

FastAPI: [запуск приложения](https://fastapi.tiangolo.com/deployment/manually/#run-a-server-manually-uvicorn)

```
uvicorn app.main:app --reload 
```

[Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html): создание миграций

```
alembic revision --autogenerate
```

[Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html): применение миграций

```
alembic upgrade head
```

Pytest: [запуск тестов](https://docs.pytest.org/en/6.2.x/usage.html)

```
pytest tests/
```

Pytest: [генерация отчета о тестовом покрытии](https://pytest-cov.readthedocs.io/en/latest/reporting.html)

```
pytest --cov-report html --cov=app tests/
```

#### Настройка pre-commit

pre-commit - очень хорошая штука, которая перед коммитами в репозиторий локально проверяет, все ли с кодом ок

Установка
```
cd main-service/
pre-commit install
```

Теперь каждый раз, когда вы захотите сделать новый коммит в репо, то pre-commit проверить его на соответствие.

Если pre-commit выбросил ошибку форматирования, то используйте след команду для автоформатирования текста
```
cd main-service/
black src
```

## Как мы работаем

### Разработка

Основной flow для работы с репозиторием и кодом приложения.
 
**Шаги:**

1. создается **Issue** с описанием нового функционала или ошибки (или выбирается уже имеющееся)
2. создается ветка на основе `develop` для выполнения задачи/части подзадач и связывается с соответствующим **Issue**
3. по завершению работы создается **Pull request (PR)** и назначается проверяющий (**Reviewers**) и ответственный за слияние (**Assignees**) - обычно один и тот же человек, но не автор **PR**
4. если все хорошо, ответственный за слияние **PR** выполняет **Merge pull request** (при необходимости можно использовать режим **Squash and merge**)

**Соглашение об именах веток:**
- `feature/<meaningful-name>` - ветки функциональностей - используются для разработки новых функций. Могут поражаться из ветки `develop` или других `feature/` веток
- `fix/<meaningful-name|issue id>` - ветки исправлений - используются для немедленного исправления ошибок. Могут поражаться из `main` или `develop` 

### Инфраструктура и администрирование

В отличие от flow [Разработка](#разработка) допускается самостоятельное слияние ветки в `main`.  

**Соглашение об именах веток:**

- `general/<meaningful-name>` - документация, изменения файлы, не связанных с кодом приложения. Может поражаться из `main`
- `devops/<meaningful-name>` - изменения конфигураций, скриптов сборки, CI/CD. Может поражаться из `main`

> Если вы один работаете над веткой, то для поддержания ее актуальности относительно `main` предпочтительнее использовать `git rebase` вместо `git merge`.

## Полезные ресурсы

**Используемые инструменты:**

- [FastAPI](https://fastapi.tiangolo.com/)
- [pydantic](https://pydantic-docs.helpmanual.io/)
- [SQLAlchemy 1.4](https://docs.sqlalchemy.org/en/14/)
- [alembic](https://alembic.sqlalchemy.org/en/latest/)

**FastAPI примеры и лучшие практики:**

- [fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices/blob/master/README.md) - содержательный список лучших практик и соглашений. Обязательно к ознакомлению.
- [Netflix/dispatch](https://github.com/Netflix/dispatch) - большое приложение реального мира от Netflix. То что вы хотите реализовать, скорее всего, уже делали там.
- [tiangolo/full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql) - комплексный пример проекта от автора FastAPI. Проект не развивается и считается устревшим - относиться скиптически.
- [apiestas](https://github.com/franloza/apiestas)
- [FastAPI-template](https://github.com/s3rius/FastAPI-template)
