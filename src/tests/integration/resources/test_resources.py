import pytest
from httpx import AsyncClient

from app.cli.db import init_dev


@pytest.fixture
def init_data():
    init_dev()


@pytest.fixture
def employees_url() -> str:
    return "/v1/employees"


@pytest.fixture
def skills_url() -> str:
    return "/v1/skills"


@pytest.fixture
def roles_url() -> str:
    return "/v1/roles"


@pytest.fixture
def grades_url() -> str:
    return "/v1/grades"


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_db", "init_data")
async def test_resources_with_skills(client: AsyncClient, employees_url: str, skills_url: str):
    """
    Use Case: работа со скиллами (навыками) сотрудников

    Author: @pppppplk
    Issue: #40
    -------------------------------
    1. просмотр списка сотрудников
    2. просмотр списка скиллов
    3. создание сотрудника
    4. просмотр списка сотрудников
    5. создание скилла
    6. обновление скиллов сотрудника
    7. просмотр списка сотрудников с фильтром по новому скиллу
    """
    # 1. просмотр списка сотрудников
    resp = await client.get(employees_url)
    employees = resp.json()["results"]
    assert resp.status_code == 200
    assert resp.json()["total"] == 8

    # 2. просмотр списка скиллов (нужны id скиллов для создания сотрудника)
    resp = await client.get(skills_url)
    skills = resp.json()
    assert resp.status_code == 200
    assert len(skills) == 13

    # 3. создание сотрудника (заполняем скиллы)
    sample_manager_id = employees[0]["id"]
    sample_role_id = employees[0]["role"]["id"]
    sample_grade_id = employees[0]["grade"]["id"]
    sample_skill_id = skills[0]["id"]

    resp = await client.post(
        employees_url,
        json={
            "first_name": "Иван",
            "last_name": "Иванов",
            "middle_name": "Иванович",
            "email": "ivanivan@yandex.ru",
            "phone": "89105678900",
            "manager_id": sample_manager_id,
            "role_id": sample_role_id,
            "grade_id": sample_grade_id,
            "skills": [{"id": sample_skill_id, "score": 2}],
        },
    )
    new_employee = resp.json()

    assert resp.status_code == 201
    assert new_employee["first_name"] == "Иван"
    assert new_employee["last_name"] == "Иванов"
    assert new_employee["middle_name"] == "Иванович"
    assert new_employee["email"] == "ivanivan@yandex.ru"
    assert new_employee["phone"] == "89105678900"
    assert new_employee["manager"]["id"] == sample_manager_id
    assert new_employee["role"]["id"] == sample_role_id
    assert new_employee["grade"]["id"] == sample_grade_id
    assert new_employee["skills"][0]["id"] == sample_skill_id
    assert new_employee["skills"][0]["score"] == 2

    # 4. просмотр списка сотрудников (проверка)
    resp = await client.get(employees_url)
    assert resp.status_code == 200
    assert resp.json()["total"] == 9

    # 5. создание скилла
    resp = await client.post(
        skills_url,
        json={
            "name": "sql",
            "max_score": 5,
        },
    )
    new_skill = resp.json()

    assert resp.status_code == 201
    assert new_skill["name"] == "sql"
    assert new_skill["max_score"] == 5

    # 6. обновление скиллов сотрудника (добавляем созданный скилл)
    resp = await client.patch(
        f"{employees_url}/{new_employee['id']}",
        json={
            "skills": [*new_employee["skills"], {"id": new_skill["id"], "score": 4}],
        },
    )
    updated_employee = resp.json()

    assert new_skill["id"] in {skill["id"] for skill in updated_employee["skills"]}
    assert resp.status_code == 200

    # 7. просмотр списка сотрудников с фильтром по новому скиллу
    resp = await client.get(employees_url, params={"skill_id": [new_skill["id"]]})
    filtered_employees = resp.json()["results"]

    assert resp.status_code == 200
    assert new_skill["id"] in {skill["id"] for skill in filtered_employees[0]["skills"]}


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_db", "init_data")
async def test_resources_with_roles_and_grades(
    client: AsyncClient,
    employees_url: str,
    roles_url: str,
    grades_url: str,
):
    # 1. Просмотр всех сотрудников

    resp = await client.get(f"/v1/employees")
    list_empl = resp.json()["results"]
    assert resp.status_code == 200
    assert resp.json()["total"] == 8

    # 2.1 Просмотр всех грейдов (нужны id для заполнения сотрудника)

    resp_sk = await client.get(f"/v1/grades")
    grades = resp_sk.json()
    assert resp_sk.status_code == 200
    assert len(resp_sk.json()) == 5

    grade_id = grades[0]["id"]
    manager_id = list_empl[0]["id"]
    role_id = list_empl[0]["role"]["id"]
    skill_id = list_empl[2]["skills"][0]["id"]

    # 2.2 Просмотр всех ролей (нужны id для заполнения сотрудника)

    resp_sk = await client.get(f"/v1/roles")
    assert resp_sk.status_code == 200
    assert len(resp_sk.json()) == 5

    # 3. Создание сотрудника (заполняем грейд и роль)

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

    # 5. Создание грейда+роли

    # Грейд
    resp_sk = await client.post(
        grades_url,
        json={
            "name": "Junior",
        },
    )

    new_grade = resp_sk.json()
    assert resp_sk.status_code == 201
    assert new_grade["name"] == "Junior"

    # Роль
    resp_sk = await client.post(
        roles_url,
        json={"name": "developer", "grades": [{"id": new_grade["id"]}]},
    )
    new_role = resp_sk.json()
    assert resp_sk.status_code == 201
    assert new_role["name"] == "developer"
    assert new_role["grades"][0]["name"] == new_grade["name"]

    # 6. Обновление грейда+роли сотрудника

    resp = await client.patch(
        f"{employees_url}/{new_employee['id']}",
        json={
            "role_id": new_role["id"],
            "grade_id": new_grade["id"],
        },
    )
    assert resp.status_code == 200
    update_employee = resp.json()
    assert new_role["id"] == update_employee["role"]["id"]
    assert new_grade["id"] == update_employee["grade"]["id"]

    # 7 Просмотр сотрудников с фильтром по новому грейду

    resp_filt_grades = await client.get(f"/v1/employees", params={"grade_id": new_grade["id"]})
    assert resp_filt_grades.status_code == 200
    assert resp_filt_grades.json()["results"][0]["grade"]["id"] == new_grade["id"]

    # 8 Просмотр сотрудников с фильтром по новой роли

    resp_filt_roles = await client.get(f"/v1/employees", params={"role_id": new_role["id"]})
    assert resp_filt_roles.status_code == 200
    assert resp_filt_roles.json()["results"][0]["role"]["id"] == new_role["id"]
