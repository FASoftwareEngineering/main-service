from app.cli.db import init_dev
from httpx import AsyncClient
import pytest


"""
0) Инициализация данных 
1) Просмотр всех сотрудников 
2) Просмотр всех Скиллов (нужны id для заполнения сотрудника) 
3) Создание сотрудника (заполняем скиллы) 
4) Просмотр всех сотрудников (проверка) 
5) Создание Скилла 
6) Обновление Скилла сотрудника 
7) Просмотр сотрудников с фильтром по новому скиллу
"""


@pytest.fixture
def init_db():
    init_dev()


@pytest.fixture
def employees_url() -> str:
    return "/v1/employees"


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("db", "init_db")
async def test_resources_with_skills(client: AsyncClient, employees_url: str):

    # 1. Просмотр всех сотрудников

    resp = await client.get(f"/v1/employees")
    list_empl = resp.json()["results"]
    assert resp.status_code == 200
    assert resp.json()["total"] == 8

    manager_id = list_empl[0]["id"]
    role_id = list_empl[0]["role"]["id"]
    grade_id = list_empl[0]["grade"]["id"]
