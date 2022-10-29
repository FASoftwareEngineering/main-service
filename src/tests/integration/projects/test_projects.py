import pytest
from httpx import AsyncClient


@pytest.fixture
def projects_url() -> str:
    return "/v1/projects"


@pytest.mark.anyio
@pytest.mark.use_case
@pytest.mark.usefixtures("db")
async def test_simple_projects(client: AsyncClient, projects_url: str):
    """
    Пример Use Case'а: простой сценарий работы с проектами
    ------------------------------------------------------
    1. просмотр списка всех проектов
    2. создание нового проекта и его просмотр
    3. возврат к списку всех проектов
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

    # 2. создание нового проекта и его просмотр
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
