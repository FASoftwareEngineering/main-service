import pytest
from httpx import AsyncClient

from app.cli.db import init_dev


@pytest.fixture
def init_data():
    init_dev()


@pytest.fixture
def skills_url() -> str:
    return "/v1/skills"


@pytest.fixture
def skills_by_id_url() -> str:
    return "/v1/skills/{value}"


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_tables_function", "init_data")
async def test_create_skill(client: AsyncClient, skills_url: str):

    resp = await client.post(
        skills_url,
        json={
            "name": "java",
            "max_score": 5,
        },
    )
    new_skill = resp.json()

    assert resp.status_code == 201
    assert new_skill["name"] == "java"
    assert new_skill["max_score"] == 5


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_tables_function", "init_data")
async def test_get_skill_by_id(client: AsyncClient, skills_by_id_url: str):

    resp = await client.get(skills_by_id_url.format(value=1))
    skill = resp.json()

    assert resp.status_code == 200
    assert skill["id"] == 1


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_tables_function", "init_data")
async def test_delete_skill_by_id(client: AsyncClient, skills_by_id_url: str):
    resp = await client.get(skills_by_id_url.format(value=1))
    assert resp.status_code == 200

    await client.delete(skills_by_id_url.format(value=1))

    resp = await client.get(skills_by_id_url.format(value=1))
    assert resp.status_code == 404


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_tables_function", "init_data")
async def test_get_skills(client: AsyncClient, skills_url: str):

    resp = await client.get(skills_url)
    skills = resp.json()

    assert resp.status_code == 200
    assert len(skills) == 13


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_tables_function", "init_data")
async def test_update_skill(client: AsyncClient, skills_url: str, skills_by_id_url: str):

    # создание скилла
    resp = await client.post(
        skills_url,
        json={
            "name": "java",
            "max_score": 5,
        },
    )
    new_skill = resp.json()

    assert resp.status_code == 201

    # обновление скилла
    resp = await client.patch(
        skills_by_id_url.format(value=new_skill["id"]),
        json={"name": "c#"},
    )
    new_skill = resp.json()

    assert resp.status_code == 200
    assert new_skill["name"] == "c#"
