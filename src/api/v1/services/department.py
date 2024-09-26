from sqlalchemy_utils import Ltree

from utils.exceptions import BadRequestException, UnauthorizedException, ForbiddenException
from utils.service import BaseService
from utils.unit_of_work import transaction_mode

from schemas.department import (
    DepartmentCreateRequestSchema,
    DepartmentUpdateRequestSchema,
    AssignManagerRequestSchema,
    DepartmentDeleteResponseSchema,
    AssignManagerResponseSchema
)
from schemas.auth import UserTokenSchema

# TODO удалить
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class DepartmentService(BaseService):

    @transaction_mode
    async def create_department(self, schema: DepartmentCreateRequestSchema, user_token_schema: UserTokenSchema):
        company = await self.uow.company.get_by_query_one_or_none(id=schema.company_id)

        if not company:
            raise BadRequestException(detail="Такой компании не существует")

        if company.id != user_token_schema.company_id:
            raise ForbiddenException(detail="Вы не являетесь администратором этой компании")

        if schema.parent_id == 0:
            schema.parent_id = None

        if schema.parent_id:
            parent_department = await self.uow.department.get_by_query_one_or_none(id=schema.parent_id)
            if not parent_department:
                raise BadRequestException(detail="Отдел с таким ID не существует")

        path = Ltree(f"company.{schema.name.replace(' ', '_')}")
        data = schema.dict()
        data['path'] = path
        return await self.uow.department.add_one_and_get_obj(**data)

    @transaction_mode
    async def update_department(self,
                                department_id: int,
                                schema: DepartmentUpdateRequestSchema,
                                user_token_schema: UserTokenSchema):
        department = await self.uow.department.get_by_query_one_or_none(id=department_id)
        if not department:
            raise BadRequestException(detail="Такого отдела не существует")

        if department.company_id != user_token_schema.company_id:
            raise ForbiddenException(detail="Вы не являетесь администратором этой компании")

        if schema.parent_id == 0:
            schema.parent_id = department.parent_id
        else:
            parent_department = await self.uow.department.get_by_query_one_or_none(id=schema.parent_id)
            if not parent_department:
                raise BadRequestException(detail="Отдел с таким ID не существует")

        new_department = await self.uow.department.update_one_by_id(obj_id=department_id,
                                                                    name=schema.name,
                                                                    parent_id=schema.parent_id)
        return await self.uow.department.get_by_query_one_or_none(id=new_department.id)

    @transaction_mode
    async def delete_department(self, department_id: int, user_token_schema: UserTokenSchema):
        department = await self.uow.department.get_by_query_one_or_none(id=department_id)
        if not department:
            raise BadRequestException(detail="Такого отдела не существует")

        if department.company_id != user_token_schema.company_id:
            raise ForbiddenException(detail="Вы не являетесь администратором этой компании")

        all_children_departments = await self.uow.department.get_by_query_all(parent_id=department_id)
        if all_children_departments:
            for child in all_children_departments:
                await self.uow.department.delete_by_query(id=child.id)

        await self.uow.department.delete_by_query(id=department_id)
        return DepartmentDeleteResponseSchema(message="Отдел успешно удален")

    @transaction_mode
    async def assign_manager(self,
                             department_id: int,
                             schema: AssignManagerRequestSchema,
                             user_token_schema: UserTokenSchema) -> AssignManagerResponseSchema:
        department = await self.uow.department.get_by_query_one_or_none(id=department_id)
        if not department:
            raise BadRequestException(detail="Такого отдела не существует")

        if department.company_id != user_token_schema.company_id:
            raise ForbiddenException(detail="Вы не являетесь администратором этой компании")

        user = await self.uow.user.get_by_query_one_or_none(id=schema.manager_id)
        if not user:
            raise BadRequestException(detail="Пользователь не найден")

        if user.company_id != department.company_id:
            raise BadRequestException(detail="Пользователь и отдел должны принадлежать одной компании")

        new_department = await self.uow.department.update_one_by_id(obj_id=department_id,
                                                                    manager_id=schema.manager_id)
        return AssignManagerResponseSchema(
            id=new_department.id,
            name=new_department.name,
            company_id=new_department.company_id,
            manager_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name
        )
