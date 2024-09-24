__all__ = [
    'router'
]

from fastapi import APIRouter

from api.v1.routers import (
    v1_auth_router,
    v1_position_router,
    v1_department_router
)

router = APIRouter()
router.include_router(v1_auth_router, prefix='/v1', tags=['Auth | V1'])
router.include_router(v1_position_router, prefix='/v1', tags=['Position | V1'])
router.include_router(v1_department_router, prefix='/v1', tags=['Department | V1'])
