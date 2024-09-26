from enum import Enum
from typing import Optional, List
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import BaseModel


class TaskStatus(Enum):
    TODO = "Задача"
    IN_PROGRESS = "В прогрессе"
    DONE = "Выполнена"


class TaskModel(BaseModel):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    responsible_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    deadline: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    status: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), default=TaskStatus.TODO)
    estimated_time: Mapped[Optional[int]] = mapped_column(Integer)

    author: Mapped["UserModel"] = relationship("UserModel",
                                               foreign_keys=[author_id],
                                               overlaps="watchers,executors")
    responsible: Mapped[Optional["UserModel"]] = relationship("UserModel", foreign_keys=[responsible_id],
                                                              overlaps="watchers,executors")

    watchers: Mapped[List["UserModel"]] = relationship(
        "UserModel",
        secondary="task_watcher",
        lazy="selectin",
        overlaps="task_watcher,task_executor",
    )
    executors: Mapped[List["UserModel"]] = relationship(
        "UserModel",
        secondary="task_executor",
        lazy="selectin",
        overlaps="task_watcher,task_executor",
    )


class TaskWatcherModel(BaseModel):
    __tablename__ = "task_watcher"

    task_id: Mapped[int] = mapped_column(Integer, ForeignKey('task.id'), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), primary_key=True)

    task = relationship("TaskModel", backref="task_watcher", overlaps="watchers,task_watcher")
    user = relationship("UserModel", overlaps="watchers,task_watcher")


class TaskExecutorModel(BaseModel):
    __tablename__ = "task_executor"

    task_id: Mapped[int] = mapped_column(Integer, ForeignKey('task.id'), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), primary_key=True)

    task = relationship("TaskModel", backref="task_executor", overlaps="executors,task_executor")
    user = relationship("UserModel", overlaps="executors,task_executor")
