import pytest
from httpx import AsyncClient

from app.cli.db import init_dev


@pytest.fixture
def init_data():
    init_dev()


@pytest.fixture
def grades_url() -> str:
    return "/v1/grades"


@pytest.fixture
def grades_by_id_url() -> str:
    return "/v1/grades/{value}"


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_db", "init_data")
async def test_create_grade(client: AsyncClient, grades_url: str):

    resp = await client.post(
        grades_url,
        json={"name": "senior1"},
    )
    new_grade = resp.json()

    assert resp.status_code == 201
    assert new_grade["name"] == "senior1"


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_db", "init_data")
async def test_get_grade_by_id(client: AsyncClient, grades_by_id_url: str):

    resp = await client.get(grades_by_id_url.format(value=1))
    grade = resp.json()

    assert resp.status_code == 200
    assert grade["id"] == 1


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_db", "init_data")
async def test_delete_grade_by_id(client: AsyncClient, grades_by_id_url: str):
    resp = await client.get(grades_by_id_url.format(value=1))
    assert resp.status_code == 200

    await client.delete(grades_by_id_url.format(value=1))

    resp = await client.get(grades_by_id_url.format(value=1))
    assert resp.status_code == 404


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_db", "init_data")
async def test_get_grades(client: AsyncClient, grades_url: str):

    resp = await client.get(grades_url)
    grades = resp.json()

    assert resp.status_code == 200
    assert len(grades) == 5


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_db", "init_data")
async def test_update_grade(client: AsyncClient, grades_url: str, grades_by_id_url: str):

    # создание грейда
    resp = await client.post(
        grades_url,
        json={"name": "senior2"},
    )
    new_grade = resp.json()

    assert resp.status_code == 201

    # обновление грейда
    resp = await client.patch(
        grades_by_id_url.format(value=new_grade["id"]),
        json={"name": "senior3"},
    )
    new_grade = resp.json()
    assert resp.status_code == 200
    assert new_grade["name"] == "senior3"
