__all__ = [
    'v1_auth_router',
    'v1_position_router',
    'v1_department_router',
    'v1_employee_router',
    'v1_task_router',
    'v1_user_router'
]

from api.v1.routers.auth import router as v1_auth_router
from api.v1.routers.position import router as v1_position_router
from api.v1.routers.department import router as v1_department_router
from api.v1.routers.employee import router as v1_employee_router
from api.v1.routers.task import router as v1_task_router
from api.v1.routers.user import router as v1_user_router
