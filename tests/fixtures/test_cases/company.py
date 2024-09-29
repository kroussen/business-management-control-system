from contextlib import nullcontext as does_not_raise
from src.models import CompanyModel
from tests.fixtures.postgres.company import COMPANIES

PARAMS_TEST_SQLALCHEMY_REPOSITORY_GET_BY_QUERY_ONE_OR_NONE = [
    ({'name': 'Tech Innovations Inc.'}, COMPANIES[0]['name'], does_not_raise())
]

PARAMS_TEST_SQLALCHEMY_REPOSITORY_GET_BY_QUERY_ALL = [
    ({'name': 'Tech Innovations Inc.'}, COMPANIES[0]['name'], does_not_raise()),
]
