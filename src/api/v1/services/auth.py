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
from utils.service import BaseService
from utils.unit_of_work import transaction_mode
from utils.auth.invite_token_utils import generate_invite_token
from utils.auth.jwt_utils import encode_jwt, decode_jwt
from utils.auth.password_utils import hash_password, validate_password
from utils.mail.service import EmailService


class AuthService(BaseService):

    @transaction_mode
    async def check_account(self, account: EmailStr) -> CheckAccountResponseSchema:
        user = await self.uow.user.get_user_by_email_or_none(email=account)
        if user:
            self.rise_400_bad_request(message="Такой e-mail уже зарегистрирован")

        invite_token = generate_invite_token()

        invite = await self.uow.invite.get_token_by_email_or_none(email=account)
        if invite:
            await self.uow.invite.update_invite_token(email=account, token=invite_token)
        else:
            await self.uow.invite.save_invite_token(email=account, token=invite_token)

        email_service = EmailService()
        await email_service.send_invite_email(account, invite_token)

        return CheckAccountResponseSchema(message='Код подтверждения отправлен на ваш e-mail', account=account)

    @transaction_mode
    async def sign_up(self, schema: SignUpRequestSchema) -> SignUpResponseSchema:
        invite = await self.uow.invite.get_token_by_email_or_none(email=schema.account)

        if invite is None:
            self.rise_400_bad_request(message="Проверьте свой аккаунт")

        if invite.token != schema.token:
            self.rise_400_bad_request(message="Неверный код подтверждения")

        await self.uow.invite.verified_account(email=schema.account)
        return SignUpResponseSchema(message="Аккаунт успешно подтвержден", account=schema.account)

    @transaction_mode
    async def sign_up_complete(self, schema: SignUpCompleteRequestSchema) -> SignUpCompleteResponseSchema:
        user = await self.uow.user.get_user_by_email_or_none(email=schema.account)
        if user:
            self.rise_400_bad_request(message="Такой пользователь уже зарегистрирован")

        company = await self.uow.company.get_company_by_name_or_none(company_name=schema.company_name)
        if company:
            self.rise_400_bad_request(message="Компания с таким именем уже существует")

        invite = await self.uow.invite.get_token_by_email_or_none(email=schema.account)
        if not invite:
            self.rise_400_bad_request(message="Подтвердите свой аккаунт"),

        new_company = await self.uow.company.create_company_and_get_object(company_name=schema.company_name)
        hashed_password = hash_password(schema.password)
        new_user = await self.uow.user.create_user_and_get_obj(
            email=schema.account,
            password=hashed_password,
            first_name=schema.first_name,
            last_name=schema.last_name,
            is_admin=True,
        )

        await self.uow.member.add_member(user_id=new_user.id, company_id=new_company.id)

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
            "email": user.email,
            "is_admin": user.is_admin,
            "iat": int(current_time.timestamp()),
        }
        token = encode_jwt(jwt_payload)
        return TokenInfoSchema(access_token=token, token_type="Bearer")

    @transaction_mode
    async def _validate_auth_user(self, email: str, password: str):
        user = await self.uow.user.get_user_by_email_or_none(email=email)

        if not user:
            self.rise_401_unauthorized(message="Неправильный e-mail или пароль")

        if not validate_password(password=password, hashed_password=user.hashed_password):
            self.rise_401_unauthorized(message="Неправильный e-mail или пароль")

        if not user.is_active:
            self.rise_403_forbidden(message="Аккаунт пользователя неактивный")

        return user

    def rise_400_bad_request(self, message):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    def rise_401_unauthorized(self, message):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)

    def rise_403_forbidden(self, message):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=message)
