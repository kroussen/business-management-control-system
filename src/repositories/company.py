from sqlalchemy import select, insert, Result

from models import CompanyModel
from utils.repository import SQLAlchemyRepository


class CompanyRepository(SQLAlchemyRepository):
    model = CompanyModel

    async def get_company_by_name_or_none(self, company_name: str) -> CompanyModel | None:
        query = select(self.model).where(self.model.name == company_name)
        res: Result = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def create_company_and_get_object(self, company_name: str) -> CompanyModel:
        query = insert(self.model).values(name=company_name).returning(self.model)
        res: Result = await self.session.execute(query)
        return res.scalar_one()