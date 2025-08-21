import uuid
from sqlalchemy import String, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum


from app.database import Base


class TaskStatus(str, Enum):
    created = "created"
    in_progress = "in_progress"
    completed = "completed"


class Task(Base):
    __tablename__ = "tasks"

    uuid: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    status: Mapped[TaskStatus] = mapped_column(SAEnum(TaskStatus, name="task_status"), default=TaskStatus.created, nullable=False)