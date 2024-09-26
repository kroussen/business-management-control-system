from utils.service import BaseService
from utils.unit_of_work import transaction_mode

from schemas.auth import UserTokenSchema
from schemas.position import (
    PositionCreateSchema,
    PositionUpdateSchema,
    PositionResponseSchema,
    DeletePositionSuccessSchema
)
from utils.exceptions import BadRequestException, UnauthorizedException, ForbiddenException

# TODO удалить
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class PositionService(BaseService):

    @transaction_mode
    async def create_position(self,
                              schema: PositionCreateSchema,
                              user_token_schema: UserTokenSchema) -> PositionResponseSchema:
        company = await self.uow.company.get_by_query_one_or_none(id=schema.company_id)

        if not company:
            raise BadRequestException(detail="Такой компании не существует")

        if company.id != user_token_schema.company_id:
            raise ForbiddenException(detail="Вы не являетесь администратором этой компании")

        position = await self.uow.position.get_by_query_one_or_none(name=schema.name)
        if position:
            raise BadRequestException(detail="Такая должность уже существует")

        data = schema.dict()
        return await self.uow.position.add_one_and_get_obj(**data)

    @transaction_mode
    async def update_position(self,
                              position_id: int,
                              schema: PositionUpdateSchema,
                              user_token_schema: UserTokenSchema) -> PositionResponseSchema:
        position = await self.uow.position.get_by_query_one_or_none(id=position_id)

        if not position:
            raise BadRequestException(detail="Такой должности не существует")

        if position.company_id != user_token_schema.company_id:
            raise ForbiddenException(detail="Вы не являетесь администратором этой компании")

        new_position = await self.uow.position.update_one_by_id(obj_id=position_id,
                                                                name=schema.name,
                                                                company_id=schema.company_id)
        return PositionResponseSchema(id=new_position.id)

    @transaction_mode
    async def delete_position(self, position_id: int, user_token_schema: UserTokenSchema) -> DeletePositionSuccessSchema:
        position = await self.uow.position.get_by_query_one_or_none(id=position_id)

        if not position:
            raise BadRequestException(detail="Такой должности не существует")

        if position.company_id != user_token_schema.company_id:
            raise ForbiddenException(detail="Вы не являетесь администратором этой компании")

        await self.uow.position.delete_by_query(id=position_id)
        return DeletePositionSuccessSchema(message="Должность удалена")
