import pytest
from httpx import AsyncClient

from app.cli.db import init_dev


@pytest.fixture
def init_data():
    init_dev()


@pytest.fixture
def projects_url() -> str:
    return "/v1/projects"


@pytest.fixture
def projects_by_id_url() -> str:
    return "/v1/projects/{value}"


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_tables_function", "init_data")
async def test_create_project(client: AsyncClient, projects_url: str):

    resp = await client.post(projects_url, json={"owner_id": 1, "code": "#PROJ 1", "name": "Проект 1"})
    new_project = resp.json()

    assert resp.status_code == 201
    assert new_project["code"] == "#PROJ 1"


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_tables_function", "init_data")
async def test_get_project_by_id(client: AsyncClient, projects_by_id_url: str):

    resp = await client.get(projects_by_id_url.format(value=1))
    project = resp.json()

    assert resp.status_code == 200
    assert project["id"] == 1


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_tables_function", "init_data")
async def test_delete_project_by_id(client: AsyncClient, projects_by_id_url: str):
    resp = await client.get(projects_by_id_url.format(value=1))
    assert resp.status_code == 200

    await client.delete(projects_by_id_url.format(value=1))

    resp = await client.get(projects_by_id_url.format(value=1))
    assert resp.status_code == 404


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_tables_function", "init_data")
async def test_get_projects(client: AsyncClient, projects_url: str):

    resp = await client.get(projects_url)
    projects = resp.json()

    assert resp.status_code == 200
    assert len(projects) == 4


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_tables_function", "init_data")
async def test_update_project(client: AsyncClient, projects_url: str, projects_by_id_url: str):

    # создание проекта
    resp = await client.post(
        projects_url,
        json={"code": f"PROJ_6", "name": f"Проект #6", "owner_id": 1},
    )
    new_project = resp.json()
    assert resp.status_code == 201

    # обновление проекта
    resp = await client.patch(
        projects_by_id_url.format(value=new_project["id"]),
        json={
            "code": f"PROJ_7",
            "name": f"Проект #7",
        },
    )
    new_project = resp.json()
    assert resp.status_code == 200
    assert new_project["code"] == "PROJ_7"
    assert new_project["name"] == "Проект #7"