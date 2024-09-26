from fastapi import APIRouter, Depends

from api.v1.services.task import TaskService
from schemas.auth import UserTokenSchema
from schemas.task import (
    TaskCreateSchema,
    TaskUpdateSchema,
    TaskResponseSchema,
    UserInfoSchema
)
from utils.auth.authorize_utils import get_current_user

router = APIRouter(prefix='/task')


@router.get("/{task_id}")
async def get_task(task_id: int,
                   service: TaskService = Depends(),
                   user_token_schema: UserTokenSchema = Depends(get_current_user)):
    return await service.get_task(task_id=task_id, user_token_schema=user_token_schema)


@router.post("/")
async def create_task(schema: TaskCreateSchema,
                      service: TaskService = Depends(),
                      user_token_schema: UserTokenSchema = Depends(get_current_user)):
    return await service.create_task(schema=schema, user_token_schema=user_token_schema)


@router.put("/{task_id}")
async def update_task(task_id: int,
                      schema: TaskUpdateSchema,
                      service: TaskService = Depends(),
                      user_token_schema: UserTokenSchema = Depends(get_current_user)):
    return await service.update_task(task_id=task_id, schema=schema, user_token_schema=user_token_schema)


@router.delete("/{task_id}")
async def delete_task(task_id: int,
                      service: TaskService = Depends(),
                      user_token_schema: UserTokenSchema = Depends(get_current_user)):
    return await service.delete_task(task_id=task_id, user_token_schema=user_token_schema)
