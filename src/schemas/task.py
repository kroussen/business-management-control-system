from datetime import date
from typing import List, Optional
from enum import Enum

from pydantic import BaseModel, Field


class TaskStatusSchema(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class UserInfoSchema(BaseModel):
    id: int
    email: str


class TaskCreateSchema(BaseModel):
    title: str
    description: Optional[str] = None
    responsible_id: Optional[int] = None
    watchers: List[int] = Field(default_factory=list)
    executors: List[int] = Field(default_factory=list)
    deadline: Optional[date] = None
    estimated_time: Optional[int] = None


class TaskUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    responsible_id: Optional[int] = None
    watchers: Optional[List[int]] = None
    executors: Optional[List[int]] = None
    deadline: Optional[date] = None
    status: Optional[TaskStatusSchema] = None
    estimated_time: Optional[int] = None


class TaskResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    author: UserInfoSchema
    responsible: Optional[UserInfoSchema]
    watchers: List[UserInfoSchema]
    executors: List[UserInfoSchema]
    deadline: date
    status: str
    estimated_time: int
    warning: Optional[str] = None


class TaskDeleteResponseSchema(BaseModel):
    message: str
