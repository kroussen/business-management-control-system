import functools
from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any, Never

from database.db import async_session_maker
from repositories import (
    UserRepository,
    CompanyRepository,
    InviteRepository,
    PositionRepository,
    DepartmentRepository,
    TaskRepository,
    TaskWatcherRepository,
    TaskExecutorRepository
)
from utils.custom_types import AsyncFunc


class AbstractUnitOfWork(ABC):

    @abstractmethod
    def __init__(self) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> Never:
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):

    def __init__(self) -> None:
        self.session_factory = async_session_maker

    async def __aenter__(self) -> None:
        self.session = self.session_factory()
        self.user = UserRepository(self.session)
        self.company = CompanyRepository(self.session)
        self.invite = InviteRepository(self.session)
        self.position = PositionRepository(self.session)
        self.department = DepartmentRepository(self.session)
        self.task = TaskRepository(self.session)
        self.task_watcher = TaskWatcherRepository(self.session)
        self.task_executor = TaskExecutorRepository(self.session)

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        if not exc_type:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


def transaction_mode(func: AsyncFunc) -> AsyncFunc:
    @functools.wraps(func)
    async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        async with self.uow:
            return await func(self, *args, **kwargs)

    return wrapper
