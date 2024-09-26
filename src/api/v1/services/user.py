from models import PositionModel, DepartmentModel
from schemas.auth import UserTokenSchema
from schemas.user import UserUpdateRequestSchema
from utils.exceptions import BadRequestException, UnauthorizedException, ForbiddenException, NotFoundException
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


class UserService(BaseService):

    @transaction_mode
    async def update_user(self, user_id: int, schema: UserUpdateRequestSchema, user_token_schema: UserTokenSchema):
        if user_id != user_token_schema.user_id:
            raise ForbiddenException(detail="Вы не можете изменить этого пользователя")

        user = await self.uow.user.get_by_query_one_or_none(id=user_id)
        if not user:
            raise NotFoundException(detail="Пользователь не найден")

        field_repo_map = {
            "department_id": (self.uow.department, DepartmentModel),
            "position_id": (self.uow.position, PositionModel),
        }

        for field, (repo, model) in field_repo_map.items():
            field_value = getattr(schema, field)
            if field_value:
                entity = await repo.get_by_query_one_or_none(id=field_value)
                if not entity:
                    raise NotFoundException(detail=f"{model.__name__} not found")
                setattr(user, field, field_value)

        update_data = schema.dict(exclude_unset=True)
        new_user = await self.uow.user.update_one_by_id(user_id, **update_data)
        return new_user
