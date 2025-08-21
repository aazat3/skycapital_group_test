from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    created = "created"
    in_progress = "in_progress"
    completed = "completed"


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: TaskStatus = TaskStatus.created


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: Optional[TaskStatus] = Field(
        default=None,
        description="Выберите статус из: created, in_progress, completed"
    )


class TaskOut(TaskBase):
    uuid: str

    class Config:
        from_attributes = True


