import pytest
from httpx import AsyncClient

from app.cli.db import init_dev


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

    skill_id = list_skill[0]["id"]
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
            "skills": [{"id": skill_id, "score": 2}],
        },
    )
    new_employee = resp.json()
    assert resp.status_code == 201
    assert new_employee["first_name"] == "Иван"
    assert new_employee["last_name"] == "Иванов"
    assert new_employee["middle_name"] == "Иванович"
    assert new_employee["email"] == "ivanivan@yandex.ru"
    assert new_employee["phone"] == "89105678900"
    assert new_employee["manager"]["id"] == manager_id
    assert new_employee["role"]["id"] == role_id
    assert new_employee["grade"]["id"] == grade_id
    assert new_employee["skills"][0]["id"] == skill_id
    assert new_employee["skills"][0]["score"] == 2

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
    new_skill_id = new_skill["id"]
    assert resp_sk.status_code == 201
    assert new_skill["name"] == "sql"
    assert new_skill["max_score"] == 5

    # 6. Обновление Скилла сотрудника

    resp = await client.patch(
        f"{employees_url}/{new_employee['id']}",
        json={
            "skills": [*new_employee["skills"], {"id": new_skill["id"], "score": 4}],
        },
    )

    update_employees = resp.json()
    assert new_skill["id"] in [skill["id"] for skill in update_employees["skills"]]
    assert resp.status_code == 200

    # 7. Просмотр сотрудников с фильтром по новому скиллу

    resp_filt_skills = await client.get(f"/v1/employees", params={"skill_id": [new_skill_id]})
    assert resp_filt_skills.status_code == 200
    empl_skills_ids = [skill["id"] for skill in resp_filt_skills.json()["results"][0]["skills"]]

    assert new_skill_id in empl_skills_ids
