from models import TaskModel, TaskWatcherModel, TaskExecutorModel
from utils.repository import SQLAlchemyRepository


class TaskRepository(SQLAlchemyRepository):
    model = TaskModel


class TaskWatcherRepository(SQLAlchemyRepository):
    model = TaskWatcherModel


class TaskExecutorRepository(SQLAlchemyRepository):
    model = TaskExecutorModel
