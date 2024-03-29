import pytest
from httpx import AsyncClient

from app.cli.db import init_dev


@pytest.fixture
def init_data():
    init_dev()


@pytest.fixture
async def example_projects_init_data(client: AsyncClient, projects_url: str):
    num_projects = 4
    projects_data = [
        {
            "code": f"PROJ_{i}",
            "name": f"Проект #{i}",
            "owner_id": 1,
        }
        for i in range(1, num_projects + 1)
    ]
    for p in projects_data:
        resp = await client.post(f"/v1/projects", json=p)
        assert resp.status_code == 201


@pytest.fixture
def projects_url() -> str:
    return "/v1/projects"


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_db", "example_projects_init_data")
@pytest.mark.skip(reason="outdated")
async def test_example_projects(client: AsyncClient, projects_url: str):
    """
    Пример Use Case'а: создание проекта
    -----------------------------------
    1. просмотр списка проектов
    2. создание проекта
    3. просмотр списка проектов
    """
    # 1. просмотр списка проектов
    resp = await client.get(f"{projects_url}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert resp_data["total"] == 4
    assert len(resp_data["results"]) == 4
    num_projects = resp_data["total"]

    # 2. создание проекта
    resp = await client.post(
        projects_url,
        json={
            "code": f"PROJ_{num_projects + 1}",
            "name": f"Проект #{num_projects + 1}",
        },
    )
    new_project = resp.json()

    assert resp.status_code == 201
    assert new_project["code"] == f"PROJ_{num_projects + 1}"
    assert new_project["name"] == f"Проект #{num_projects + 1}"
    assert new_project["status"] == "default"
    assert new_project["start_date"] is None
    assert new_project["end_date"] is None
    assert new_project["contract_price"] is None

    # 3. просмотр списка проектов
    resp = await client.get(f"{projects_url}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert resp_data["total"] == num_projects + 1
    assert len(resp_data["results"]) == num_projects + 1


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("runtime_db", "init_data")
@pytest.mark.skip(reason="incomplete")
async def test_update_project(client: AsyncClient, projects_url: str):
    """
    Use Case: редактирование и закрытие проекта

    Author: @Osetinskiy-pokemon
    Issue: #39 #53
    --------------
    1. просмотр списка проектов
    2. создание проекта
    3. просмотр списка проектов
    4. просмотр карточки проекта
    5. закрытие проекта
    6. просмотр списка проектов
    7. просмотр списка сотрудников с фильтром status == closed
    """
    # первоначальная настройка сервиса (может быть общей для нескольких тестов)
    num_projects = 4
    projects_data = [
        {
            "code": f"PROJ_{i}",
            "name": f"Проект #{i}",
        }
        for i in range(1, num_projects + 1)
    ]
    for p in projects_data:
        resp = await client.post(f"/v1/projects", json=p)
        assert resp.status_code == 201

    # 1. просмотр списка всех проектов
    resp = await client.get(f"{projects_url}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert resp_data["total"] == num_projects
    assert len(resp_data["results"]) == num_projects

    # 2. создание нового проекта
    resp = await client.post(
        projects_url,
        json={
            "code": f"PROJ_{num_projects + 1}",
            "name": f"Проект #{num_projects + 1}",
        },
    )
    new_project = resp.json()

    assert resp.status_code == 201
    assert new_project["code"] == f"PROJ_{num_projects + 1}"
    assert new_project["name"] == f"Проект #{num_projects + 1}"
    assert new_project["status"] == "default"
    assert new_project["start_date"] is None
    assert new_project["end_date"] is None
    assert new_project["contract_price"] is None

    # 3. возврат к списку всех проектов
    resp = await client.get(f"{projects_url}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert resp_data["total"] == num_projects + 1
    assert len(resp_data["results"]) == num_projects + 1

    # 4. поиск проекта по id
    resp = await client.get(f"{projects_url}/{new_project['id']}")
    assert resp.status_code == 200

    # 5. изменение атрибута status полученного проекта на closed
    resp = await client.patch(f"{projects_url}/{new_project['id']}", json={"data": {"status": "closed"}})

    assert new_project["status"] == "closed"
    assert resp.status_code == 200

    # 6. возврат к списку всех проектов
    resp = await client.get(f"{projects_url}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert resp_data["total"] == num_projects + 1
    assert len(resp_data["results"]) == num_projects + 1

    # 7. получение проектов по фильтру атрибута status == closed
    resp_filt_status = await client.get(f"{projects_url}", params={"status": "closed"})
    assert resp_filt_status.status_code == 200
    assert resp_filt_status.json()["results"][0]["projects"][0]["id"] == new_project["id"]
