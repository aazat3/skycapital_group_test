from fastapi import FastAPI


from app.config import settings
from app.database import init_db
from app.routers import tasks


app = FastAPI(title=settings.PROJECT_NAME)


app.include_router(tasks.router)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
async def root():
    return {"service": settings.PROJECT_NAME, "docs": "/docs"}