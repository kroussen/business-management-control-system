from datetime import datetime, timezone

from fastapi import HTTPException, status
from pydantic import EmailStr

from schemas.auth import (
    SignUpRequestSchema,
    SignUpResponseSchema,
    SignUpCompleteRequestSchema,
    SignUpCompleteResponseSchema,
    CheckAccountResponseSchema,
    SignInRequestSchema,
    TokenInfoSchema
)
from utils.auth.invite_token_utils import generate_invite_token
from utils.auth.jwt_utils import encode_jwt, decode_jwt
from utils.auth.password_utils import hash_password, validate_password
from utils.exceptions import BadRequestException, UnauthorizedException, ForbiddenException
from utils.mail.service import EmailService
from utils.service import BaseService
from utils.unit_of_work import transaction_mode

# TODO удалить
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# TODO удалить


class AuthService(BaseService):

    @transaction_mode
    async def check_account(self, account: EmailStr) -> CheckAccountResponseSchema:
        user = await self.uow.user.get_by_query_one_or_none(email=account)
        if user:
            raise BadRequestException(detail="Такой e-mail уже зарегистрирован")

        invite_token = generate_invite_token()

        invite = await self.uow.invite.get_by_query_one_or_none(email=account)

        if invite.is_verified:
            raise BadRequestException(detail="Ваш аккаунт уже подтвержден")

        if invite:
            await self.uow.invite.update_one_by_id(obj_id=invite.id, email=account, token=invite_token)
        else:
            await self.uow.invite.add_one(email=account, token=invite_token)

        email_service = EmailService()
        await email_service.send_invite_email(account, invite_token)

        return CheckAccountResponseSchema(message='Код подтверждения отправлен на ваш e-mail', account=account)

    @transaction_mode
    async def sign_up(self, schema: SignUpRequestSchema) -> SignUpResponseSchema:
        invite = await self.uow.invite.get_by_query_one_or_none(email=schema.account)

        if invite is None:
            raise BadRequestException(detail="Проверьте свой аккаунт")

        if invite.token != schema.token:
            raise BadRequestException(detail="Неверный код подтверждения")

        await self.uow.invite.update_one_by_id(obj_id=invite.id, is_verified=True)
        return SignUpResponseSchema(message="Аккаунт успешно подтвержден", account=schema.account)

    @transaction_mode
    async def sign_up_complete(self, schema: SignUpCompleteRequestSchema) -> SignUpCompleteResponseSchema:

        user = await self.uow.user.get_by_query_one_or_none(email=schema.account)
        if user:
            raise BadRequestException(detail="Такой пользователь уже зарегистрирован")

        company = await self.uow.company.get_by_query_one_or_none(name=schema.company_name)
        if company:
            raise BadRequestException(detail="Компания с таким именем уже существует")

        invite = await self.uow.invite.get_by_query_one_or_none(email=schema.account)
        if not invite:
            raise BadRequestException(detail="Проверьте свой аккаунт")

        hashed_password = hash_password(schema.password)
        new_company_id = await self.uow.company.add_one_and_get_id(name=schema.company_name)
        new_position_id = await self.uow.position.add_one_and_get_id(name='Admin', company_id=new_company_id)

        new_user = {
            'email': schema.account,
            'first_name': schema.first_name,
            'last_name': schema.last_name,
            'hashed_password': hashed_password,
            'is_admin': True,
            'company_id': new_company_id,
            'position_id': new_position_id
        }

        await self.uow.user.add_one(**new_user)

        return SignUpCompleteResponseSchema(
            account=schema.account,
            password=hashed_password,
            first_name=schema.first_name,
            last_name=schema.last_name,
            company_name=schema.company_name,
        )

    @transaction_mode
    async def sign_in(self, schema: SignInRequestSchema) -> TokenInfoSchema:
        user = await self._validate_auth_user(schema.account, schema.password)

        current_time = datetime.now(timezone.utc)
        jwt_payload = {
            "sub": str(user.id),
            "company_id": user.company_id,
            "is_admin": user.is_admin,
            "is_active": user.is_active,
            "iat": int(current_time.timestamp()),
        }
        token = encode_jwt(jwt_payload)
        return TokenInfoSchema(access_token=token, token_type="Bearer")

    @transaction_mode
    async def _validate_auth_user(self, email: str, password: str):
        user = await self.uow.user.get_by_query_one_or_none(email=email)

        if not user:
            raise UnauthorizedException(detail="Неправильный e-mail или пароль")

        if not validate_password(password=password, hashed_password=user.hashed_password):
            raise UnauthorizedException(detail="Неправильный e-mail или пароль")

        if not user.is_active:
            raise ForbiddenException(detail="Аккаунт пользователя неактивный")

        return user
