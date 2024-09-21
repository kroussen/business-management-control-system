from sqlalchemy import select, insert, Result

from models import CompanyModel
from utils.repository import SQLAlchemyRepository


class CompanyRepository(SQLAlchemyRepository):
    model = CompanyModel
