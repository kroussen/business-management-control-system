from pydantic import EmailStr
from sqlalchemy import select, insert, Result

from models import UserModel
from utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = UserModel

    async def get_user_by_email_or_none(self, email: str) -> UserModel:
        query = select(self.model).where(self.model.email == email)
        res: Result = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def create_user_and_get_obj(self,
                                      email: EmailStr,
                                      password: str,
                                      first_name: str,
                                      last_name: str,
                                      is_admin: bool) -> None:
        query = insert(self.model).values(email=email,
                                          first_name=first_name,
                                          last_name=last_name,
                                          is_admin=is_admin,
                                          hashed_password=password).returning(self.model)
        res: Result = await self.session.execute(query)
        return res.scalar_one()
