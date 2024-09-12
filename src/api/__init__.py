__all__ = [
    'router'
]

from fastapi import APIRouter

from api.v1.routers import (
    v1_auth_router
)

router = APIRouter()
router.include_router(v1_auth_router, prefix='/v1', tags=['Auth | V1'])
