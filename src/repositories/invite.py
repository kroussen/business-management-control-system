from models import InviteModel
from utils.repository import SQLAlchemyRepository


class InviteRepository(SQLAlchemyRepository):
    model = InviteModel
