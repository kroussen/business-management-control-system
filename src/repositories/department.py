from models import DepartmentModel
from utils.repository import SQLAlchemyRepository


class DepartmentRepository(SQLAlchemyRepository):
    model = DepartmentModel
