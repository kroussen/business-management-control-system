from fastapi import APIRouter, Depends

from api.v1.services.position import PositionService
from schemas.position import (
    PositionCreateSchema,
    PositionUpdateSchema,
    PositionResponseSchema,
    DeletePositionSuccessSchema
)
from schemas.auth import UserTokenSchema
from utils.auth.authorize_utils import is_user_admin

router = APIRouter(prefix='/position')


@router.post("/create_position", response_model=PositionResponseSchema)
async def create_position(schema: PositionCreateSchema,
                          service: PositionService = Depends(),
                          user_token_schema: UserTokenSchema = Depends(is_user_admin)) -> PositionResponseSchema:
    return await service.create_position(schema=schema, user_token_schema=user_token_schema)


@router.put("/{position_id}", response_model=PositionResponseSchema)
async def update_position(position_id: int,
                          schema: PositionUpdateSchema,
                          service: PositionService = Depends(),
                          user_token_schema: UserTokenSchema = Depends(is_user_admin)) -> PositionResponseSchema:
    return await service.update_position(position_id=position_id, schema=schema, user_token_schema=user_token_schema)


@router.delete("/{position_id}", response_model=DeletePositionSuccessSchema)
async def delete_position(position_id: int,
                          service: PositionService = Depends(),
                          user_token_schema: UserTokenSchema = Depends(is_user_admin)) -> DeletePositionSuccessSchema:
    return await service.delete_position(position_id=position_id, user_token_schema=user_token_schema)
