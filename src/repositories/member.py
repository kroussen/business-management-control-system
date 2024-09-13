from sqlalchemy import insert

from models import MemberModel
from utils.repository import SQLAlchemyRepository


class MemberRepository(SQLAlchemyRepository):
    model = MemberModel

    async def add_member(self, user_id: int, company_id: int) -> None:
        query = insert(self.model).values(user_id=user_id, company_id=company_id)
        await self.session.execute(query)
