from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import BaseModel


class UserModel(BaseModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey('company.id'))
    position_id: Mapped[int] = mapped_column(Integer, ForeignKey('position.id'))
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey('department.id'), nullable=True)
    company = relationship("CompanyModel", back_populates="employees")
    position = relationship("PositionModel", back_populates="employees")
    department = relationship("DepartmentModel",
                              back_populates='employees',
                              foreign_keys=[department_id])
