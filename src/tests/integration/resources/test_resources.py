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
    Use Case: работа со скиллами (навыками) сотрудника

    Author: @pppppplk
    Issue: #40 #53
    --------------
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
    employees_data = resp.json()
    employees = employees_data["results"]

    assert resp.status_code == 200
    assert employees_data["total"] == 8

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

    assert resp.status_code == 200
    assert new_skill["id"] in {skill["id"] for skill in updated_employee["skills"]}

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
    """
    Use Case: работа с ролями и грейдами сотрудника

    Author: @ruki011
    Issue: #40 #53
    --------------
    1. просмотр списка сотрудников
    2.1 просмотр списка грейдов
    2.2 просмотр списка ролей
    3. создание сотрудника
    4. просмотр списка сотрудников
    5.1. создание грейдов
    5.2. создание роли
    6. обновление роли и грейда сотрудника
    7. просмотр списка сотрудников с фильтром по новой роли
    8. просмотр списка сотрудников с фильтром по новому грейду
    """
    # 1. просмотр списка сотрудников
    resp = await client.get(employees_url)
    employees_data = resp.json()
    employees = employees_data["results"]

    assert resp.status_code == 200
    assert employees_data["total"] == 8

    # 2.1 просмотр списка грейдов
    resp = await client.get(grades_url)
    grades = resp.json()
    assert resp.status_code == 200
    assert len(grades) == 5

    # 2.2 просмотр списка ролей
    resp = await client.get(f"/v1/roles")
    roles = resp.json()
    assert resp.status_code == 200
    assert len(roles) == 5

    # 3. создание сотрудника
    sample_manager_id = employees[0]["id"]
    sample_role_id = roles[2]["id"]
    sample_grade_id = roles[2]["grades"][1]["id"]

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

    # 4. просмотр списка сотрудников (проверка)
    resp = await client.get(employees_url)
    assert resp.status_code == 200
    assert resp.json()["total"] == 9

    # 5.1. создание грейдов
    new_grades = []
    for grade_name in ["junior+", "middle+"]:
        resp = await client.post(grades_url, json={"name": grade_name})
        new_grade = resp.json()
        assert resp.status_code == 201
        assert new_grade["name"] == grade_name
        new_grades.append(new_grade)

    # 5.2. создание роли
    resp = await client.post(
        roles_url,
        json={
            "name": "developer",
            "grades": [{"id": grade["id"]} for grade in new_grades],
        },
    )
    new_role = resp.json()

    assert resp.status_code == 201
    assert new_role["name"] == "developer"
    assert len(new_role["grades"]) == len(new_grades)
    for grade, expected in zip(new_role["grades"], new_grades):
        assert grade["name"] == expected["name"]

    # 6. обновление роли и грейда сотрудника
    new_grade = new_grades[0]

    resp = await client.patch(
        f"{employees_url}/{new_employee['id']}",
        json={
            "role_id": new_role["id"],
            "grade_id": new_grade["id"],
        },
    )
    updated_employee = resp.json()

    assert resp.status_code == 200
    assert updated_employee["role"]["id"] == new_role["id"]
    assert updated_employee["grade"]["id"] == new_grade["id"]

    # 7. просмотр списка сотрудников с фильтром по новой роли
    resp = await client.get(employees_url, params={"grade_id": new_grade["id"]})
    filtered_employees = resp.json()["results"]

    assert resp.status_code == 200
    assert filtered_employees[0]["grade"]["id"] == new_grade["id"]

    # 8. просмотр списка сотрудников с фильтром по новому грейду
    resp = await client.get(employees_url, params={"role_id": new_role["id"]})
    filtered_employees = resp.json()["results"]

    assert resp.status_code == 200
    assert filtered_employees[0]["role"]["id"] == new_role["id"]
