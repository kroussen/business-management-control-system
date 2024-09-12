__all__ = [
    'v1_auth_router',
    'v1_department_router',
    'v1_employee_router',
    'v1_position_router',
    'v1_task_router',
    'v1_user_router'
]

from api.v1.routers.auth import router as v1_auth_router
