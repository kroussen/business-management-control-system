from fastapi import APIRouter, Depends

from api.v1.services.department import DepartmentService
from schemas.department import (
    DepartmentCreateRequestSchema,
    DepartmentUpdateRequestSchema,
    AssignManagerRequestSchema
)
from schemas.auth import UserTokenSchema
from utils.auth.authorize_utils import is_user_admin

router = APIRouter(prefix='/department')


@router.post("/")
async def create_department(
        schema: DepartmentCreateRequestSchema,
        service: DepartmentService = Depends(),
        user_token_schema: UserTokenSchema = Depends(is_user_admin)):
    return await service.create_department(schema=schema, user_token_schema=user_token_schema)


@router.put("/{department_id}")
async def update_department(
        department_id: int,
        schema: DepartmentUpdateRequestSchema,
        service: DepartmentService = Depends(),
        user_token_schema: UserTokenSchema = Depends(is_user_admin)):
    return await service.update_department(department_id=department_id,
                                           schema=schema,
                                           user_token_schema=user_token_schema)


@router.delete("/{department_id}")
async def delete_department(
        department_id: int,
        service: DepartmentService = Depends(),
        user_token_schema: UserTokenSchema = Depends(is_user_admin)):
    return await service.delete_department(department_id=department_id, user_token_schema=user_token_schema)


@router.patch("/{department_id}/assign_manager")
async def assign_manager(
        department_id: int,
        schema: AssignManagerRequestSchema,
        service: DepartmentService = Depends(),
        user_token_schema: UserTokenSchema = Depends(is_user_admin)):
    return await service.assign_manager(department_id=department_id, schema=schema, user_token_schema=user_token_schema)
