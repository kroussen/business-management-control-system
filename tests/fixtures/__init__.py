__all__ = [
    'FakeBaseService',
    'FakeUnitOfWork',
    'FakeAuthService',
    'FakeUserService',
    'FakeTaskService',
    'FakePositionService',
    'FakeEmployeeService',
    'FakeDepartmentService',
    'postgres'
]

from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

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
from src.api.v1.services.auth import AuthService
from src.api.v1.services.user import UserService
from src.api.v1.services.position import PositionService
from src.api.v1.services.task import TaskService
from src.api.v1.services.employee import EmployeeService
from src.api.v1.services.department import DepartmentService
from src.utils.service import BaseService
from src.utils.unit_of_work import UnitOfWork
from src.utils.mail.service import EmailService
from tests.fixtures import postgres


class FakeUnitOfWork(UnitOfWork):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    async def __aenter__(self) -> None:
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
        await self._session.flush()


class FakeBaseService(BaseService):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.uow = FakeUnitOfWork(session)


class FakeUserService(FakeBaseService, UserService):
    base_repository: str = 'user'


class FakeAuthService(FakeBaseService, AuthService):
    pass


class FakePositionService(FakeBaseService, PositionService):
    base_repository: str = 'position'


class FakeTaskService(FakeBaseService, TaskService):
    base_repository: str = 'task'


class FakeEmployeeService(FakeBaseService, EmployeeService):
    base_repository: str = 'employee'


class FakeDepartmentService(FakeBaseService, DepartmentService):
    base_repository: str = 'department'


class FakeEmailService(FakeBaseService, EmailService):
    pass
