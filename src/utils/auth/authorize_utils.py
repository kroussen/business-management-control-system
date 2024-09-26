from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from schemas.auth import UserTokenSchema
from utils.auth.jwt_utils import decode_jwt
from utils.exceptions import UnauthorizedException, ForbiddenException

http_bearer = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> UserTokenSchema:
    token = credentials.credentials
    payload: dict = decode_jwt(token=token)
    user_id: int = payload.get('sub')
    company_id: int = payload.get('company_id')
    is_admin: bool = payload.get('is_admin')
    is_active: bool = payload.get('is_active')

    if user_id is None:
        raise UnauthorizedException(detail='Не удалось проверить учетные данные')

    if not is_active:
        raise ForbiddenException(detail='Аккаунт не активен')

    return UserTokenSchema(user_id=user_id, company_id=company_id, is_admin=is_admin)


async def is_user_admin(user_token_schema: UserTokenSchema = Depends(get_current_user)) -> UserTokenSchema:
    if not user_token_schema.is_admin:
        raise ForbiddenException(detail='Вы не являетесь администратором')
    return user_token_schema
