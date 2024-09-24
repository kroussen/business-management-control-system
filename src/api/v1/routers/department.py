from fastapi import APIRouter, Depends

from api.v1.services.department import DepartmentService
from schemas.department import (
    DepartmentCreateRequestSchema,
    DepartmentUpdateRequestSchema,
    AssignManagerRequestSchema
)

router = APIRouter(prefix='/department')


@router.post("/")
async def create_department(schema: DepartmentCreateRequestSchema, service: DepartmentService = Depends()):
    return await service.create_department(schema=schema)


@router.put("/{department_id}")
async def update_department(department_id: int,
                            schema: DepartmentUpdateRequestSchema,
                            service: DepartmentService = Depends()):
    return await service.update_department(department_id=department_id, schema=schema)


@router.delete("/{department_id}")
async def delete_department(department_id: int, service: DepartmentService = Depends()):
    return await service.delete_department(department_id=department_id)


@router.patch("/{department_id}/assign_manager")
async def assign_manager(department_id: int,
                         schema: AssignManagerRequestSchema,
                         service: DepartmentService = Depends()):
    return await service.assign_manager(department_id=department_id, schema=schema)


@router.get("/hierarchy")
async def get_department_hierarchy():
    return 200
