from fastapi import Request
from fastapi.responses import HTMLResponse
from pydantic import EmailStr

from schemas.auth import UserTokenSchema
from schemas.employee import (
    CreateEmployeeRequestSchema,
    GenerateEmployeeInviteResponseSchema,
    CompleteEmployeeRegistrationRequestSchema,
    CompleteEmployeeRegistrationResponseSchema,
    EmployeeDataResponseSchema,
    UpdateEmployeeRequestSchema,
    RebindEmailRequestSchema,
    RebindEmailResponseSchema,
    ConfirmRebindEmailRequestSchema
)
from utils.auth.invite_token_utils import generate_invite_token
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


class EmployeeService(BaseService):

    @transaction_mode
    async def create_employee(self, schema: CreateEmployeeRequestSchema, user_token_schema: UserTokenSchema):
        employee = await self.uow.user.get_by_query_one_or_none(email=schema.email)
        if employee:
            raise BadRequestException(detail="Сотрудник с таким e-mail уже зарегистрирован")

        new_employee = await self.uow.user.add_one_and_get_obj(
            email=schema.email,
            first_name=schema.first_name,
            last_name=schema.last_name,
            company_id=user_token_schema.company_id,
            is_admin=False,
            is_active=False,
            position_id=schema.position_id
        )

        return new_employee

    @transaction_mode
    async def generate_employee_invite(self, employee_id: int, user_token_schema: UserTokenSchema, request: Request):
        employee = await self.uow.user.get_by_query_one_or_none(id=employee_id)
        if not employee:
            raise BadRequestException(detail="Сотрудник не найден")

        if employee.company_id != user_token_schema.company_id:
            raise ForbiddenException(detail="Вы не являетесь администратором этой компании")

        invite_token = generate_invite_token()

        invite = await self.uow.invite.get_by_query_one_or_none(email=employee.email)

        if invite:
            await self.uow.invite.update_one_by_id(obj_id=invite.id, email=employee.email, token=invite_token)
        else:
            await self.uow.invite.add_one(email=employee.email, token=invite_token)

        base_url = request.base_url
        invite_url = f"{base_url}api/v1/employee/registration-complete?email={employee.email}"

        email_service = EmailService()
        await email_service.send_invite_employee(employee.email, invite_url)
        return GenerateEmployeeInviteResponseSchema(message="Приглашение отправлено",
                                                    email=employee.email)

    @transaction_mode
    async def show_registration_form(self, email: EmailStr):
        employee = await self.uow.user.get_by_query_one_or_none(email=email)
        if not employee:
            raise BadRequestException(detail="Сотрудник не найден")

        invite = await self.uow.invite.get_by_query_one_or_none(email=email)
        if not invite:
            raise ForbiddenException(detail="Ошибка приглашения")

        html_content = f"""
                    <form method="post">
                        <p>Email: {email}</p>
                        <input type="hidden" name="email" value="{email}">
                        <input type="password" name="password" placeholder="Password" required>
                        <input type="password" name="password_confirm" placeholder="Confirm Password" required>
                        <button type="submit">Завершить регистрацию</button>
                    </form>
                    """
        return HTMLResponse(content=html_content)

    @transaction_mode
    async def complete_employee_registration(self, schema: CompleteEmployeeRegistrationRequestSchema):
        employee = await self.uow.user.get_by_query_one_or_none(email=schema.email)
        if not employee:
            raise BadRequestException(detail="Сотрудник не найден")

        if employee.is_active:
            raise BadRequestException(detail="Такой пользователь уже зарегистрирован")

        if schema.password != schema.password_confirm:
            raise BadRequestException(detail="Пароли не совпадают")

        hashed_password = hash_password(schema.password)

        invite = await self.uow.invite.get_by_query_one_or_none(email=schema.email)

        if not invite:
            raise ForbiddenException(detail="Ошибка приглашения")

        await self.uow.invite.update_one_by_id(obj_id=invite.id, is_verified=True)
        await self.uow.user.update_one_by_id(obj_id=employee.id,
                                             is_active=True,
                                             hashed_password=hashed_password)
        response_data = EmployeeDataResponseSchema(
            email=employee.email,
            first_name=employee.first_name,
            last_name=employee.last_name,
            is_admin=employee.is_admin,
            is_active=employee.is_active,
            company_id=employee.company_id,
        )

        return CompleteEmployeeRegistrationResponseSchema(message="Аккаунт успешно создан", data=response_data)

    @transaction_mode
    async def update_employee_data(self, schema: UpdateEmployeeRequestSchema, user_token_schema: UserTokenSchema):
        employee = await self.uow.user.get_by_query_one_or_none(id=user_token_schema.user_id)
        if not employee:
            raise BadRequestException(detail='Сотрудник не найден')

        if not validate_password(schema.current_password, employee.hashed_password):
            raise BadRequestException(detail='Неправильный пароль')

        position = await self.uow.position.get_by_query_one_or_none(id=schema.position_id)
        if not position:
            raise BadRequestException(detail='Такой должности не существует')

        new_employee_data = {
            'first_name': schema.first_name,
            'last_name': schema.last_name,
            'position_id': schema.position_id
        }

        updated_employee = await self.uow.user.update_one_by_id(obj_id=user_token_schema.user_id, **new_employee_data)
        return updated_employee

    @transaction_mode
    async def rebind_email(self, schema: RebindEmailRequestSchema, user_token_schema: UserTokenSchema):
        user = await self.uow.user.get_by_query_one_or_none(id=user_token_schema.user_id)
        if not user:
            raise BadRequestException(detail="Пользователь не найден")

        if not validate_password(schema.current_password, user.hashed_password):
            raise BadRequestException(detail="Неправильный пароль")

        email_exist = await self.uow.user.get_by_query_one_or_none(email=schema.new_email)
        if email_exist:
            raise BadRequestException(detail='Такой email уже занят')

        invite = await self.uow.invite.get_by_query_one_or_none(email=user.email)
        token = generate_invite_token()
        await self.uow.invite.update_one_by_id(obj_id=invite.id, email=schema.new_email, is_verified=False, token=token)

        email_service = EmailService()
        await email_service.send_invite_email(schema.new_email, token)

        return RebindEmailResponseSchema(email=schema.new_email, message="Код подтверждения отправлен на ваш e-mail")

    @transaction_mode
    async def confirm_rebind_email(self, schema: ConfirmRebindEmailRequestSchema, user_token_schema: UserTokenSchema):
        invite = await self.uow.invite.get_by_query_one_or_none(email=schema.email)
        if not invite:
            raise BadRequestException(detail='Такой email не найден')

        user = await self.uow.user.get_by_query_one_or_none(id=user_token_schema.user_id)

        if invite.token != schema.token:
            raise BadRequestException(detail='Неверный код подтверждения')

        await self.uow.invite.update_one_by_id(obj_id=invite.id, is_verified=True)
        await self.uow.user.update_one_by_id(obj_id=user.id, email=schema.email)

        return RebindEmailResponseSchema(email=schema.email, message='Почта успешно подтверждена')
