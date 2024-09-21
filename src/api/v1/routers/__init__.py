__all__ = [
    'v1_auth_router',
    'v1_position_router',
]

from api.v1.routers.auth import router as v1_auth_router
from api.v1.routers.position import router as v1_position_router
