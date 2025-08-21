# Tasks API (FastAPI + SQLAlchemy + Pydantic + Docker + Pytest)

Минимальный CRUD-сервис управления задачами со статусами `created | in_progress | completed`.

## Быстрый старт (Docker Compose)
```bash
docker compose up --build

http://localhost:8000/docs
```
## Запуск тестов 
```bash
pip install -r requirements.txt
pytest -v -s