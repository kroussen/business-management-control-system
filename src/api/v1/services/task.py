from schemas.auth import UserTokenSchema
from schemas.task import (
    TaskCreateSchema,
    TaskUpdateSchema,
    TaskResponseSchema,
    UserInfoSchema,
    TaskDeleteResponseSchema
)
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


class TaskService(BaseService):

    @transaction_mode
    async def create_task(self, schema: TaskCreateSchema, user_token_schema: UserTokenSchema):
        user = await self.uow.user.get_by_query_one_or_none(id=user_token_schema.user_id)
        if not user:
            raise NotFoundException(detail="Пользователь не найден")

        if schema.responsible_id:
            responsible_user = await self.uow.user.get_by_query_one_or_none(id=schema.responsible_id)

            if not responsible_user:
                raise NotFoundException(detail="Ответственный не найден")

        new_task = await self.uow.task.add_one_and_get_obj(
            title=schema.title,
            description=schema.description,
            author_id=user_token_schema.user_id,
            responsible_id=schema.responsible_id,
            deadline=schema.deadline,
            estimated_time=schema.estimated_time,
        )

        for watcher_id in schema.watchers:
            watcher = await self.uow.user.get_by_query_one_or_none(id=watcher_id)
            if watcher:
                await self.uow.task_watcher.add_one(task_id=new_task.id, user_id=watcher_id)

        for executor_id in schema.executors:
            executor = await self.uow.user.get_by_query_one_or_none(id=watcher_id)
            if executor:
                await self.uow.task_executor.add_one(task_id=new_task.id, user_id=executor_id)

        watchers = [
            UserInfoSchema(id=watcher.id, email=watcher.email)
            for watcher_id in schema.watchers
            if (watcher := await self.uow.user.get_by_query_one_or_none(id=watcher_id))
        ]

        executors = [
            UserInfoSchema(id=executor.id, email=executor.email)
            for executor_id in schema.executors
            if (executor := await self.uow.user.get_by_query_one_or_none(id=executor_id))
        ]

        task_response = TaskResponseSchema(
            id=new_task.id,
            title=new_task.title,
            description=new_task.description,
            author=UserInfoSchema(id=user.id, email=user.email),
            responsible=(
                UserInfoSchema(id=responsible_user.id, email=responsible_user.email)
                if responsible_user
                else None
            ),
            watchers=watchers,
            executors=executors,
            deadline=new_task.deadline,
            status=new_task.status,
            estimated_time=new_task.estimated_time,
        )

        return task_response

    @transaction_mode
    async def get_task(self, task_id: int, user_token_schema: UserTokenSchema):
        task = await self.uow.task.get_by_query_one_or_none(id=task_id)
        if not task:
            raise NotFoundException(detail="Задача не найдена")

        return task

    @transaction_mode
    async def update_task(self, task_id: int, schema: TaskUpdateSchema, user_token_schema: UserTokenSchema):
        author = await self.uow.user.get_by_query_one_or_none(id=user_token_schema.user_id)
        if not author:
            raise BadRequestException(detail="Автор не найден")

        if schema.responsible_id:
            responsible_user = await self.uow.user.get_by_query_one_or_none(id=schema.responsible_id)

            if not responsible_user:
                raise NotFoundException(detail="Ответственный не найден")

        update_data = schema.dict(exclude_unset=True)

        if "watchers" in update_data:
            await self.uow.task_watcher.delete_by_query(task_id=task_id)
            for watcher_id in update_data["watchers"]:
                watcher = await self.uow.user.get_by_query_one_or_none(id=watcher_id)
                if watcher:
                    await self.uow.task_watcher.add_one(task_id=task_id, user_id=watcher_id)

        if "executors" in update_data:
            await self.uow.task_executor.delete_by_query(task_id=task_id)
            for executor_id in update_data["executors"]:
                executor = await self.uow.user.get_by_query_one_or_none(id=executor_id)
                if executor:
                    await self.uow.task_executor.add_one(task_id=task_id, user_id=executor_id)

        updated_task = await self.uow.task.get_by_query_one_or_none(id=task_id)
        return updated_task

    @transaction_mode
    async def delete_task(self, task_id: int, user_token_schema: UserTokenSchema):
        task = await self.uow.task.get_by_query_one_or_none(id=task_id)
        if not task:
            raise NotFoundException(detail="Задача не найдена")

        if task.author_id != user_token_schema.user_id:
            raise ForbiddenException(detail="Только автор задачи может ее удалить")

        await self.uow.task_executor.delete_by_query(task_id=task_id)
        await self.uow.task_watcher.delete_by_query(task_id=task_id)
        await self.uow.task.delete_by_query(id=task_id)
        return TaskDeleteResponseSchema(message="Задача успешно удалена")
