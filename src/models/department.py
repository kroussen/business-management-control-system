from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Ltree, LtreeType

from models import BaseModel


class DepartmentModel(BaseModel):
    __tablename__ = 'department'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    path: Mapped[Ltree] = mapped_column(LtreeType, nullable=False)

    company_id: Mapped[int] = mapped_column(Integer, ForeignKey('company.id'))
    manager_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=True)
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey('department.id'), nullable=True)

    company = relationship('CompanyModel', back_populates='departments')
    manager = relationship('UserModel', foreign_keys=[manager_id])
    employees = relationship('UserModel',
                             back_populates='department',
                             foreign_keys='UserModel.department_id')
