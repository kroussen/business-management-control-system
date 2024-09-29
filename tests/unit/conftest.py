from collections.abc import Sequence
from copy import deepcopy

import pytest
import pytest_asyncio
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import CompanyModel, UserModel, DepartmentModel, InviteModel, PositionModel, TaskModel
from src.utils.custom_types import AsyncFunc
from tests import fixtures
from tests.utils import bulk_save_models

# TODO удалить
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# TODO удалить


@pytest_asyncio.fixture
async def setup_companies(transaction_session: AsyncSession, companies: tuple[dict]) -> None:
    """Setup companies in the database."""
    await bulk_save_models(transaction_session, CompanyModel, companies)


@pytest_asyncio.fixture
async def setup_users(setup_companies: None, transaction_session: AsyncSession, users: tuple[dict]) -> None:
    """Setup users in the database."""
    await bulk_save_models(transaction_session, UserModel, users)


@pytest_asyncio.fixture
async def setup_departments(setup_companies: None, transaction_session: AsyncSession, departments: tuple[dict]) -> None:
    """Setup departments in the database."""
    await bulk_save_models(transaction_session, DepartmentModel, departments)


@pytest_asyncio.fixture
async def setup_invites(transaction_session: AsyncSession, invites: tuple[dict]) -> None:
    """Setup invites in the database."""
    logger.debug(f'Setting up {invites}')
    await bulk_save_models(transaction_session, InviteModel, invites)
    logger.debug("Successfully")


@pytest_asyncio.fixture
async def setup_positions(setup_companies: None, transaction_session: AsyncSession, positions: tuple[dict]) -> None:
    """Setup positions in the database."""
    await bulk_save_models(transaction_session, PositionModel, positions)


@pytest_asyncio.fixture
async def setup_tasks(transaction_session: AsyncSession, tasks: tuple[dict]) -> None:
    """Setup tasks in the database."""
    await bulk_save_models(transaction_session, TaskModel, tasks)


@pytest_asyncio.fixture
def get_first_company(transaction_session: AsyncSession) -> AsyncFunc:
    """Retrieve all users from the database."""

    async def _get_companies() -> Sequence[CompanyModel]:
        res: Result = await transaction_session.execute(select(CompanyModel))
        return res.scalar()

    return _get_companies


@pytest_asyncio.fixture
def companies() -> tuple[dict]:
    return deepcopy(fixtures.postgres.COMPANIES)


@pytest_asyncio.fixture
def users() -> tuple[dict]:
    return deepcopy(fixtures.postgres.USERS)


@pytest_asyncio.fixture
def departments() -> tuple[dict]:
    return deepcopy(fixtures.postgres.DEPARTMENTS)


@pytest_asyncio.fixture
def invites() -> tuple[dict]:
    return deepcopy(fixtures.postgres.INVITES)


@pytest_asyncio.fixture
def positions() -> tuple[dict]:
    return deepcopy(fixtures.postgres.POSITIONS)


@pytest_asyncio.fixture
def tasks() -> tuple[dict]:
    return deepcopy(fixtures.postgres.TASKS)


@pytest.fixture
def first_user() -> dict:
    return deepcopy(fixtures.postgres.USERS[0])


@pytest.fixture
def first_company() -> dict:
    return deepcopy(fixtures.postgres.COMPANIES[0])


@pytest.fixture
def first_department() -> dict:
    return deepcopy(fixtures.postgres.DEPARTMENTS[0])


@pytest.fixture
def first_invite() -> dict:
    return deepcopy(fixtures.postgres.INVITES[0])


@pytest.fixture
def first_position() -> dict:
    return deepcopy(fixtures.postgres.POSITIONS[0])


@pytest.fixture
def first_task() -> dict:
    return deepcopy(fixtures.postgres.TASKS[0])
