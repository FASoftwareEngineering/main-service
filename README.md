# main-service

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
```pyton
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
