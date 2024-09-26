from typing import Optional
from pydantic import BaseModel


class UserUpdateRequestSchema(BaseModel):
    department_id: Optional[int]
    position_id: Optional[int]