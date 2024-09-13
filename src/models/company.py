from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import BaseModel


class CompanyModel(BaseModel):
    __tablename__ = 'company'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    users: Mapped[list["UserModel"]] = relationship(secondary='member', back_populates='companies')
