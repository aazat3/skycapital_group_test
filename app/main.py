from fastapi import FastAPI
from config import settings
from database import init_db
from routers import tasks


app = FastAPI(title=settings.PROJECT_NAME)


app.include_router(tasks.router)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
async def root():
    return {"service": settings.PROJECT_NAME, "docs": "/docs"}