import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_crud_flow(async_client: AsyncClient):
    # Create
    r = await async_client.post("/tasks/", json={"title": "Test", "description": "Desc"})
    assert r.status_code == 201, r.text
    item = r.json()
    task_uuid = item["uuid"]
    assert item["status"] == "created"

    # Get
    r = await async_client.get(f"/tasks/{task_uuid}")
    assert r.status_code == 200
    assert r.json()["title"] == "Test"

    # Patch
    r = await async_client.patch(f"/tasks/{task_uuid}", json={"status": "in_progress", "title": "New"})
    assert r.status_code == 200
    assert r.json()["status"] == "in_progress"
    assert r.json()["title"] == "New"

    # Delete
    r = await async_client.delete(f"/tasks/{task_uuid}")
    assert r.status_code == 204

    # Get wrong uuid
    r = await async_client.get(f"/tasks/{task_uuid}")
    assert r.status_code == 404

    # Patch wrong uuid
    r = await async_client.patch(f"/tasks/{task_uuid}", json={"status": "in_progress", "title": "New"})
    assert r.status_code == 404

    # Get wrong uuid
    r = await async_client.delete(f"/tasks/{task_uuid}")
    assert r.status_code == 404
    
@pytest.mark.asyncio
async def test_create_invalid_task(async_client: AsyncClient):
    # Missing title
    r = await async_client.post("/tasks/", json={"description": "No title"})
    assert r.status_code == 422 

    # Empty payload
    r = await async_client.post("/tasks/", json={})
    assert r.status_code == 422

@pytest.mark.asyncio
async def test_list_tasks_and_filter(async_client: AsyncClient):
    tasks = [
        {"title": "Task1", "description": "A", "status": "created"},
        {"title": "Task2", "description": "B", "status": "in_progress"},
        {"title": "Task3", "description": "C", "status": "done"},
    ]
    [await async_client.post("/tasks/", json=t) for t in tasks]

    # List all tasks
    r = await async_client.get("/tasks/")
    assert r.status_code == 200
    data = r.json()
    assert len(data) >= 3

    # Filter by status
    r = await async_client.get("/tasks/?status_filter=in_progress")
    assert r.status_code == 200
    data = r.json()
    assert all(task["status"] == "in_progress" for task in data)

@pytest.mark.asyncio
async def test_pagination(async_client: AsyncClient):
    [await async_client.post("/tasks/", json={"title": f"T{i}", "description": "Desc"}) for i in range(5)]   

    # Limit
    r = await async_client.get("/tasks/?limit=2")
    assert r.status_code == 200
    assert len(r.json()) == 2

    # Offset
    r = await async_client.get("/tasks/?limit=2&offset=2")
    assert r.status_code == 200
    assert len(r.json()) == 2  