from datetime import datetime
from typing import Annotated
from sqlalchemy import String, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from collections.abc import AsyncGenerator


from config import settings


DATABASE_URL_asyncpg = settings.DATABASE_URL_asyncpg
async_engine  = create_async_engine(DATABASE_URL_asyncpg)
async_session_factory  = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine, expire_on_commit=False)


# Базовый класс базы данных
class Base(DeclarativeBase):
    pass


async def init_db():
    from app import models # noqa: F401
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Функция для получения сессии
async def get_session() -> AsyncGenerator:
    async with async_session_factory() as session:
        yield session