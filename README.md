# Tasks API (FastAPI + SQLAlchemy + Pydantic + Docker + Pytest)

Минимальный CRUD-сервис управления задачами со статусами `created | in_progress | completed`.

## Быстрый старт (Docker Compose)
```bash
docker compose up --build

http://localhost:8000/docs
```
## Запуск тестов 
```bash
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v -s
```

## Adminer (управление базой)
```bash
http://localhost:8080
```

## Увидеть работу приложения можно по адресу: 
```bash
http://aazatserver.ru:8000/docs
```