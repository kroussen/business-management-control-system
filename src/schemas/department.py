from typing import Optional
from pydantic import BaseModel


class DepartmentCreateRequestSchema(BaseModel):
    name: str
    company_id: int
    parent_id: Optional[int] = None


class DepartmentUpdateRequestSchema(BaseModel):
    name: Optional[str] = None
    parent_id: int | None = None


class AssignManagerRequestSchema(BaseModel):
    manager_id: int


class AssignManagerResponseSchema(BaseModel):
    id: int
    name: str
    company_id: int
    manager_id: int
    first_name: str
    last_name: str


class DepartmentDeleteResponseSchema(BaseModel):
    message: str
