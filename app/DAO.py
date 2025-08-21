from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List


import models, schemas


async def create_task(db: AsyncSession, payload: schemas.TaskCreate) -> models.Task:
    task = models.Task(title=payload.title, description=payload.description)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_task(db: AsyncSession, task_id: str) -> models.Task | None:
    return await db.get(models.Task, task_id)


async def list_tasks(db: AsyncSession, limit: int = 50, offset: int = 0, status_filter: schemas.TaskStatus | None = None) -> List[models.Task]:
    stmt = select(models.Task)
    if status_filter:
        stmt = stmt.filter(models.Task.status == status_filter)
    stmt = stmt.offset(offset).limit(limit)
    res = await db.execute(stmt)
    return res.scalars().all()


async def update_task(db: AsyncSession, task: models.Task, payload: schemas.TaskUpdate) -> models.Task:
    if payload.title is not None:
        task.title = payload.title
    if payload.description is not None:
        task.description = payload.description
    if payload.status is not None:
        task.status = payload.status

    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, task: models.Task) -> None:
    await db.delete(task)
    await db.commit()