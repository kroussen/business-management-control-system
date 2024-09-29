__all__ = [
    'COMPANIES',
    'DEPARTMENTS',
    'INVITES',
    'POSITIONS',
    'TASKS', 'TASK_WATCHERS', 'TASK_EXECUTORS',
    'USERS'
]

from tests.fixtures.postgres.company import COMPANIES
from tests.fixtures.postgres.department import DEPARTMENTS
from tests.fixtures.postgres.invite import INVITES
from tests.fixtures.postgres.position import POSITIONS
from tests.fixtures.postgres.task import TASKS, TASK_WATCHERS, TASK_EXECUTORS
from tests.fixtures.postgres.user import USERS
