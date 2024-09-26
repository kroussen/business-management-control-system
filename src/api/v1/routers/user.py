from fastapi import APIRouter, Depends

from api.v1.services.user import UserService
from schemas.auth import UserTokenSchema
from schemas.user import UserUpdateRequestSchema
from utils.auth.authorize_utils import get_current_user

router = APIRouter(prefix="/user")


@router.patch("/{user_id}")
async def update_user(user_id: int,
                      schema: UserUpdateRequestSchema,
                      service: UserService = Depends(),
                      user_token_schema: UserTokenSchema = Depends(get_current_user)):
    return await service.update_user(user_id=user_id, schema=schema, user_token_schema=user_token_schema)
