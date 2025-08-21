import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


from app.main import app
from app.database import Base, get_session


# Тестовая БД — SQLite (async) файл, чтобы избежать проблем с in-memory и несколькими соединениями
TEST_DB_URL = "sqlite+aiosqlite:///./test_tasks.db"
engine = create_async_engine(TEST_DB_URL, future=True)
TestingSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture(autouse=True, scope="module")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Переопределяем зависимость БД
@app.dependency_overrides[get_session]
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


@pytest.mark.anyio
async def test_crud_flow():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create
        r = await client.post("/tasks/", json={"title": "Test", "description": "Desc"})
        assert r.status_code == 201, r.text
        item = r.json()
        task_id = item["id"]
        assert item["status"] == "created"


        # Get
        r = await client.get(f"/tasks/{task_id}")
        assert r.status_code == 200
        assert r.json()["title"] == "Test"


        # List
        r = await client.get("/tasks/?limit=10&offset=0")
        assert r.status_code == 200
        assert any(t["id"] == task_id for t in r.json())


        # Update
        r = await client.put(f"/tasks/{task_id}", json={"status": "in_progress", "title": "New"})
        assert r.status_code == 200
        assert r.json()["status"] == "in_progress"
        assert r.json()["title"] == "New"


        # Delete
        r = await client.delete(f"/tasks/{task_id}")
        assert r.status_code == 204


        # Not found after delete
        r = await client.get(f"/tasks/{task_id}")
        assert r.status_code == 404