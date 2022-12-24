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
def employees_by_id_url() -> str:
    return "/v1/employees/{value}"


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_db", "init_data")
async def test_create_employee(client: AsyncClient, employees_url: str):
    # получение менеджеров из начального наполнения
    resp_e = await client.get(f"/v1/employees")
    managers = resp_e.json()['results']

    print(managers)

    # получение роли из начального наполнения
    resp_r = await client.get(f"/v1/roles")
    roles = resp_r.json()

    # получение грейдов из начального наполнения
    resp_g = await client.get(f"/v1/grades")
    grades = resp_g.json()

    # получение скиллов из начального наполнения
    resp_s = await client.get(f"/v1/skills")
    skills = resp_s.json()
    our_skills = [skills[0], skills[1]]

    resp = await client.post(
        employees_url,
        json={
            "first_name": "Кирилл",
            "last_name": "Фонарев",
            "middle_name": "Иванович",
            "email": "ivani@yandex.ru",
            "phone": "89705678900",
            "manager_id": managers[0]["id"],
            "role_id": roles[0]["id"],
            "grade_id": grades[0]["id"],
            "skills": [{"id": skill["id"], "score": 2} for skill in our_skills],
        },
    )
    new_employee = resp.json()

    assert resp.status_code == 201
    assert new_employee["first_name"] == "Кирилл"
    assert new_employee["last_name"] == "Фонарев"
    assert new_employee["middle_name"] == "Иванович"
    assert new_employee["email"] == "ivani@yandex.ru"
    assert new_employee["phone"] == "89705678900"
    assert new_employee["manager"]['id'] == managers[0]["id"]
    assert new_employee["role"]["id"] == roles[0]["id"]
    assert new_employee["grade"]["id"] == grades[0]["id"]
    assert len(new_employee["skills"]) == len(our_skills)
    for skill, expected in zip(
        sorted(new_employee["skills"], key=lambda x: x["id"]), sorted(our_skills, key=lambda x: x["id"])
    ):
        assert skill["id"] == expected["id"]
        assert skill["score"] == 2


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_db", "init_data")
async def test_get_employee_by_id(client: AsyncClient, employees_by_id_url: str):

    resp = await client.get(employees_by_id_url.format(value=5))
    employee = resp.json()

    assert resp.status_code == 200
    assert employee["id"] == 5


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_db", "init_data")
async def test_delete_employee_by_id(client: AsyncClient, employees_by_id_url: str):
    resp = await client.get(employees_by_id_url.format(value=5))
    assert resp.status_code == 200

    await client.delete(employees_by_id_url.format(value=5))

    resp = await client.get(employees_by_id_url.format(value=5))
    assert resp.status_code == 404


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_db", "init_data")
async def test_get_employees(client: AsyncClient, employees_url: str):

    resp = await client.get(employees_url)
    employees_data = resp.json()

    assert resp.status_code == 200
    assert employees_data["total"] == 8


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_db", "init_data")
async def test_update_employee(client: AsyncClient, employees_url: str, employees_by_id_url: str):
    # создание сотрудника

    # получение роли из начального наполнения
    resp_r = await client.get(f"/v1/roles")
    roles = resp_r.json()

    # получение грейдов из начального наполнения
    resp_g = await client.get(f"/v1/grades")
    grades = resp_g.json()

    resp = await client.post(
        employees_url,
        json={
            "first_name": "Мария",
            "last_name": "Иванова",
            "middle_name": "Олеговна",
            "email": "ivn@yandex.ru",
            "phone": "89103389000",
            "role_id": roles[0]["id"],
            "grade_id": grades[0]["id"],

        },
    )
    new_employee = resp.json()

    assert resp.status_code == 201

    # обновление фамилии сотрудника
    resp = await client.patch(
        employees_by_id_url.format(value=new_employee["id"]),
        json={"last_name": "Шишкина"},
    )
    new_employee = resp.json()
    assert resp.status_code == 200
    assert new_employee["last_name"] == "Шишкина"
