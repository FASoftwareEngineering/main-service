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


@pytest.fixture
def skills_url() -> str:
    return "/v1/skills"


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("db", "init_db")
async def test_resources_with_skills(client: AsyncClient, employees_url: str, skills_url: str):
    # 1. Просмотр всех сотрудников

    resp = await client.get(f"/v1/employees")
    list_empl = resp.json()["results"]
    assert resp.status_code == 200
    assert resp.json()["total"] == 8

    # 2. Просмотр всех Скиллов (нужны id для заполнения сотрудника)

    resp_sk = await client.get(f"/v1/skills")
    list_skill = resp_sk.json()
    assert resp_sk.status_code == 200
    assert len(resp_sk.json()) == 13

    skills_id = list_skill[0]["id"]
    manager_id = list_empl[0]["id"]
    role_id = list_empl[0]["role"]["id"]
    grade_id = list_empl[0]["grade"]["id"]

    # 3. Создание сотрудника (заполняем скиллы)

    resp = await client.post(
        employees_url,
        json={
            "first_name": "Иван",
            "last_name": "Иванов",
            "middle_name": "Иванович",
            "email": "ivanivan@yandex.ru",
            "phone": "89105678900",
            "manager_id": manager_id,
            "role_id": role_id,
            "grade_id": grade_id,
            "skills": [{"id": skills_id, "score": 2}],
        },
    )
    new_employees = resp.json()
    assert resp.status_code == 201
    assert new_employees["first_name"] == "Иван"
    assert new_employees["last_name"] == "Иванов"
    assert new_employees["middle_name"] == "Иванович"
    assert new_employees["email"] == "ivanivan@yandex.ru"
    assert new_employees["phone"] == "89105678900"
    assert new_employees["manager"]["id"] == manager_id
    assert new_employees["role"]["id"] == role_id
    assert new_employees["grade"]["id"] == grade_id
    assert new_employees["skills"][0]["id"] == skills_id
    assert new_employees["skills"][0]["score"] == 2

    # 4. Просмотр всех сотрудников (проверка)

    resp = await client.get(f"/v1/employees")
    assert resp.status_code == 200
    assert resp.json()["total"] == 9

    # 5. Создание Скилла

    resp_sk = await client.post(
        skills_url,
        json={
            "name": "sql",
            "max_score": 5,
        },
    )
    new_skill = resp_sk.json()
    assert resp_sk.status_code == 201
    assert new_skill["name"] == "sql"
    assert new_skill["max_score"] == 5

    # 6. Обновление Скилла сотрудника

    resp = await client.patch(
        f"{employees_url}/{new_employees['id']}",
        json={
            "skills": [*new_employees["skills"], {"id": new_skill["id"], "score": 4}],
        },
    )

    update_employees = resp.json()
    skill_is_present = False
    for skill in update_employees["skills"]:
        if skill["id"] == new_skill["id"]:
            skill_is_present = True
            break

    assert skill_is_present
    assert resp.status_code == 200

    # 7. Просмотр сотрудников с фильтром по новому скиллу

    resp_filt_skills = await client.get(f"/v1/employees", params={"skill_id": [14]})
    assert resp_filt_skills.status_code == 200
    assert resp_filt_skills.json()["results"][0]["skills"][0]["id"] == 14