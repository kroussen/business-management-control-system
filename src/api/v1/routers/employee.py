from fastapi import APIRouter, Depends, Request, Form
from pydantic import EmailStr

from api.v1.services.employee import EmployeeService
from schemas.auth import UserTokenSchema
from schemas.employee import (
    CreateEmployeeRequestSchema,
    CompleteEmployeeRegistrationRequestSchema,
    UpdateEmployeeRequestSchema,
    RebindEmailRequestSchema,
    ConfirmRebindEmailRequestSchema
)
from utils.auth.authorize_utils import get_current_user, is_user_admin

router = APIRouter(prefix='/employee')


@router.post("/create")
async def create_employee(
        schema: CreateEmployeeRequestSchema,
        service: EmployeeService = Depends(),
        user_token_schema: UserTokenSchema = Depends(is_user_admin)):
    return await service.create_employee(schema=schema, user_token_schema=user_token_schema)


@router.post("/{employee_id}/invite")
async def generate_employee_invite(
        employee_id: int,
        request: Request,
        service: EmployeeService = Depends(),
        user_token_schema: UserTokenSchema = Depends(is_user_admin)):
    return await service.generate_employee_invite(employee_id=employee_id,
                                                  user_token_schema=user_token_schema,
                                                  request=request)


@router.get("/registration-complete")
async def show_registration_form(
        email: EmailStr,
        service: EmployeeService = Depends()):
    return await service.show_registration_form(email=email)


@router.post("/registration-complete")
async def complete_employee_registration(
        schema: CompleteEmployeeRegistrationRequestSchema,
        service: EmployeeService = Depends()):
    return await service.complete_employee_registration(schema=schema)


@router.patch("/update")
async def update_employee_data(
        schema: UpdateEmployeeRequestSchema,
        service: EmployeeService = Depends(),
        user_token_schema: UserTokenSchema = Depends(get_current_user)):
    return await service.update_employee_data(schema=schema, user_token_schema=user_token_schema)


@router.post("/rebind-email")
async def rebind_email(
        schema: RebindEmailRequestSchema,
        service: EmployeeService = Depends(),
        user_token_schema: UserTokenSchema = Depends(get_current_user)):
    return await service.rebind_email(schema=schema, user_token_schema=user_token_schema)


@router.post("/confirm-rebind-email")
async def confirm_rebind_email(
        schema: ConfirmRebindEmailRequestSchema,
        service: EmployeeService = Depends(),
        user_token_schema: UserTokenSchema = Depends(get_current_user)):
    return await service.confirm_rebind_email(schema=schema, user_token_schema=user_token_schema)
