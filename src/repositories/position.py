from models import PositionModel
from utils.repository import SQLAlchemyRepository


class PositionRepository(SQLAlchemyRepository):
    model = PositionModel
