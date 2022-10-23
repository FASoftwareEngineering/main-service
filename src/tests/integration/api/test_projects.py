# import pytest
# from httpx import AsyncClient
#
#
# @pytest.mark.anyio
# async def test_get_proget_404(client: AsyncClient):
#     project_id = 999
#     response = await client.get(f"/v1/projects/{project_id}")
#     assert response.status_code == 404
#     assert response.json() == {"detail": [{"msg": f"Project with id={project_id} not found"}]}
