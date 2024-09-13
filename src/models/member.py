from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import BaseModel


class MemberModel(BaseModel):
    __tablename__ = 'member'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey('company.id'))
