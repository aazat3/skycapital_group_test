from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from database import get_session
import schemas
import DAO


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(payload: schemas.TaskCreate, db: AsyncSession = Depends(get_session)):
    return await DAO.create_task(db, payload)


@router.get("/{task_id}", response_model=schemas.TaskOut)
async def get_task(task_id: str, db: AsyncSession = Depends(get_session)):
    task = await DAO.get_task(db, task_id)
    if not task:
         HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/", response_model=List[schemas.TaskOut])
async def list_tasks(
    db: AsyncSession = Depends(get_session),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    status_filter: schemas.TaskStatus | None = Query(None, description="Filte by status"),
    ):
    return await DAO.list_tasks(db, limit=limit, offset=offset, status_filter=status_filter)


@router.put("/{task_id}", response_model=schemas.TaskOut)
async def update_task(task_id: str, payload: schemas.TaskUpdate, db: AsyncSession = Depends(get_session)):
    task = DAO.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return await DAO.update_task(db, task, payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, db: AsyncSession = Depends(get_session)):
    task = DAO.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await DAO.delete_task(db, task)
    return None