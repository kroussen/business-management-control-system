from pydantic import BaseModel


class PositionBaseSchema(BaseModel):
    name: str
    company_id: int


class PositionCreateSchema(PositionBaseSchema):
    pass


class PositionUpdateSchema(PositionCreateSchema):
    pass


class PositionResponseSchema(BaseModel):
    id: int


class DeletePositionSuccessSchema(BaseModel):
    message: str
