# import pytest
# from httpx import AsyncClient


# @pytest.mark.asyncio
# async def test_create_task(async_client: AsyncClient):
#     payload = {"title": "Test task1", "description": "Test description"}
#     await async_client.post("/tasks/", json=payload)
#     response = await async_client.get("/tasks/")
#     print("/////////////////////////////////////////////////////")
#     print(response.json())
#     # assert response.status_code == 200
#     # data = response.json()
#     # assert data["title"] == payload["title"]
#     # assert data["description"] == payload["description"]
#     # assert "id" in data