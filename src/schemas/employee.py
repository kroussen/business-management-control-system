from pydantic import BaseModel, EmailStr
from typing import Optional


class CreateEmployeeRequestSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    position_id: int


class GenerateEmployeeInviteResponseSchema(BaseModel):
    message: str
    email: EmailStr


class CompleteEmployeeRegistrationRequestSchema(BaseModel):
    email: str
    password: str
    password_confirm: str


class EmployeeDataResponseSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    is_admin: bool
    is_active: bool
    company_id: int


class CompleteEmployeeRegistrationResponseSchema(BaseModel):
    message: str
    data: EmployeeDataResponseSchema


class UpdateEmployeeRequestSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    position_id: Optional[int] = None
    current_password: str


class RebindEmailRequestSchema(BaseModel):
    new_email: EmailStr
    current_password: str


class RebindEmailResponseSchema(BaseModel):
    email: EmailStr
    message: str


class ConfirmRebindEmailRequestSchema(BaseModel):
    email: EmailStr
    token: str
