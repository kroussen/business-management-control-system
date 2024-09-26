from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import LtreeType, Ltree

from models import BaseModel


class PositionModel(BaseModel):
    __tablename__ = "position"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey('company.id'), nullable=False)

    company = relationship("CompanyModel", back_populates="positions")
    employees = relationship("UserModel", back_populates="position")
