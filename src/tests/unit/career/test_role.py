import pytest
from httpx import AsyncClient

from app.cli.db import init_dev


@pytest.fixture
def init_data():
    init_dev()


@pytest.fixture
def roles_url() -> str:
    return "/v1/roles"


@pytest.fixture
def roles_by_id_url() -> str:
    return "/v1/roles/{value}"


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_db", "init_data")
async def test_create_role(client: AsyncClient, roles_url: str):

    # получение грейдов из начального наполнения
    resp = await client.get(f"/v1/grades")
    grades = resp.json()
    our_grades = [grades[0], grades[1]]

    # создание роли
    resp = await client.post(
        roles_url,
        json={"name": "cashier", "grades": [{"id": grade["id"]} for grade in our_grades]},
    )
    new_role = resp.json()

    assert resp.status_code == 201
    assert new_role["name"] == "cashier"
    assert len(new_role["grades"]) == 2


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_db", "init_data")
async def test_get_role_by_id(client: AsyncClient, roles_by_id_url: str):

    resp = await client.get(roles_by_id_url.format(value=1))
    role = resp.json()

    assert resp.status_code == 200
    assert role["id"] == 1


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_db", "init_data")
async def test_delete_role_by_id(client: AsyncClient, roles_by_id_url: str):
    resp = await client.get(roles_by_id_url.format(value=1))
    assert resp.status_code == 200

    await client.delete(roles_by_id_url.format(value=1))

    resp = await client.get(roles_by_id_url.format(value=1))
    assert resp.status_code == 404


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_db", "init_data")
async def test_get_roles(client: AsyncClient, roles_url: str):

    resp = await client.get(roles_url)
    roles = resp.json()

    assert resp.status_code == 200
    assert len(roles) == 5


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_db", "init_data")
async def test_update_role(client: AsyncClient, roles_url: str, roles_by_id_url: str):

    # создание роли
    resp = await client.post(
        roles_url,
        json={"name": "assistent"},
    )
    new_role = resp.json()

    assert resp.status_code == 201

    # обновление роли
    resp = await client.patch(
        roles_by_id_url.format(value=new_role["id"]),
        json={"name": "assistent2"},
    )
    new_role = resp.json()
    assert resp.status_code == 200
    assert new_role["name"] == "assistent2"
