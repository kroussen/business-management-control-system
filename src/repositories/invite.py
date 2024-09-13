from pydantic import EmailStr
from sqlalchemy import select, insert, update, Result

from models import InviteModel
from utils.repository import SQLAlchemyRepository


class InviteRepository(SQLAlchemyRepository):
    model = InviteModel

    async def get_token_by_email_or_none(self, email: EmailStr) -> InviteModel:
        query = select(self.model).where(self.model.email == email)
        res: Result = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def save_invite_token(self, email: EmailStr, token: str) -> None:
        query = insert(self.model).values(email=email, token=token)
        await self.session.execute(query)

    async def update_invite_token(self, email: EmailStr, token: str) -> None:
        query = update(self.model).values(token=token).where(self.model.email == email)
        await self.session.execute(query)

    async def verified_account(self, email: EmailStr) -> None:
        query = update(self.model).values(is_verified=True).where(self.model.email == email)
        await self.session.execute(query)
