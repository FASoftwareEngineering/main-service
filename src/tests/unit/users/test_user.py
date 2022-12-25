import pytest
from httpx import AsyncClient

from app.cli.db import init_dev


@pytest.fixture
def init_data():
    init_dev()


@pytest.fixture
def users_url() -> str:
    return "/v1/users"


@pytest.fixture
def users_by_id_url() -> str:
    return "/v1/users/{value}"


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_tables_function", "init_data")
async def test_create_user(client: AsyncClient, users_url: str):

    resp = await client.post(
        users_url,
        json={
            "type": f"employee",
            "sso_id": f"USER_1",
            "email": f"user@mail.ru",
            "phone": f"89999999999",
            "first_name": f"Ivan",
            "last_name": f"Ivanov",
        },
    )
    new_user = resp.json()

    assert resp.status_code == 201
    assert new_user["type"] == "employee"
    assert new_user["sso_id"] == "USER_1"
    assert new_user["email"] == "user@mail.ru"
    assert new_user["phone"] == "89999999999"
    assert new_user["first_name"] == "Ivan"
    assert new_user["last_name"] == "Ivanov"


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_tables_function", "init_data")
async def test_get_user_by_id(client: AsyncClient, users_by_id_url: str):

    resp = await client.get(users_by_id_url.format(value=1))
    user = resp.json()

    assert resp.status_code == 200
    assert user["id"] == 1


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_tables_function", "init_data")
async def test_delete_user_by_id(client: AsyncClient, users_by_id_url: str):
    resp = await client.get(users_by_id_url.format(value=1))
    assert resp.status_code == 200

    await client.delete(users_by_id_url.format(value=1))

    resp = await client.get(users_by_id_url.format(value=1))
    assert resp.status_code == 404


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_tables_function", "init_data")
async def test_get_users(client: AsyncClient, users_url: str):

    resp = await client.get(users_url)
    users = resp.json()

    assert resp.status_code == 200
    assert len(users) == 4


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_tables_function", "init_data")
async def test_update_user(client: AsyncClient, users_url: str, users_by_id_url: str):

    # создание пользователя
    resp = await client.post(
        users_url,
        json={
            "type": f"employee",
            "sso_id": f"USER_2",
            "email": f"user2@mail.ru",
            "phone": f"89999999997",
            "first_name": f"Petr",
            "last_name": f"Petrov",
        },
    )
    new_user = resp.json()
    assert resp.status_code == 201

    # обновление пользователя
    resp = await client.patch(
        users_by_id_url.format(value=new_user["id"]),
        json={
            "first_name": f"Artur",
        },
    )
    new_user = resp.json()
    assert resp.status_code == 200
    assert new_user["first_name"] == "Artur"
