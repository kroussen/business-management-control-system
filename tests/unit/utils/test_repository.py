from typing import Any

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import CompanyModel
from src.utils.repository import SQLAlchemyRepository
from src.utils.custom_types import AsyncFunc

from tests.fixtures import test_cases
from tests.fixtures.postgres.company import COMPANIES


class TestSqlAlchemyRepository:
    class _SqlAlchemyRepository(SQLAlchemyRepository):
        model = CompanyModel

    def __get_sql_rep(self, session: AsyncSession) -> SQLAlchemyRepository:
        return self._SqlAlchemyRepository(session)

    async def test_add_one(self, transaction_session: AsyncSession,
                           first_company: dict,
                           get_first_company: AsyncFunc) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        await sql_rep.add_one(**first_company)
        await transaction_session.flush()

        company_in_db: Sequence[CompanyModel] = await get_first_company()
        assert company_in_db.name == first_company['name']

    async def test_add_one_and_get_id(
            self,
            transaction_session: AsyncSession,
            first_company: dict,
            get_first_company: AsyncFunc,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        company_id = await sql_rep.add_one_and_get_id(**first_company)
        assert company_id == first_company.get('id')
        await transaction_session.flush()

    async def test_add_one_and_get_obj(
            self,
            transaction_session: AsyncSession,
            first_company: dict,
            get_first_company: AsyncFunc,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        company = await sql_rep.add_one_and_get_obj(**first_company)
        assert company.id == first_company.get('id')
        await transaction_session.flush()

    @pytest.mark.usefixtures('setup_companies')
    @pytest.mark.parametrize(
        ('values', 'expected_result', 'expectation'),
        test_cases.company.PARAMS_TEST_SQLALCHEMY_REPOSITORY_GET_BY_QUERY_ONE_OR_NONE,
    )
    async def test_get_by_query_one_or_none(
            self,
            values: dict,
            expected_result: CompanyModel,
            expectation: Any,
            transaction_session: AsyncSession,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        with expectation:
            result: UserModel | None = await sql_rep.get_by_query_one_or_none(**values)
            assert result.name == expected_result

    @pytest.mark.usefixtures('setup_companies')
    async def test_get_by_query_all(self, transaction_session: AsyncSession) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        companies_in_db: Sequence[CompanyModel] = await sql_rep.get_by_query_all()
        assert len(companies_in_db) == len(COMPANIES)
        assert companies_in_db[0].name == COMPANIES[0].get('name')


    # @pytest.mark.usefixtures('setup_companies')
    # async def test_update_one_by_id(self, transaction_session: AsyncSession) -> None:
    #     sql_rep = self.__get_sql_rep(transaction_session)
    #
    #     updated_user: UserModel | None = await sql_rep.update_one_by_id(values.pop('_id'), **values)
    #     assert updated_user.to_pydantic_schema() == expected_result
    #
    # @pytest.mark.usefixtures('setup_users')
    # @pytest.mark.parametrize(
    #     ('values', 'expected_result', 'expectation'),
    #     fixtures.test_cases.PARAMS_TEST_SQLALCHEMY_REPOSITORY_DELETE_BY_QUERY,
    # )
    # async def test_delete_by_query(
    #         self,
    #         values: dict,
    #         expected_result: list,
    #         expectation: Any,
    #         transaction_session: AsyncSession,
    #         get_users: AsyncFunc,
    # ) -> None:
    #     sql_rep = self.__get_sql_rep(transaction_session)
    #     with expectation:
    #         await sql_rep.delete_by_query(**values)
    #         await transaction_session.flush()
    #         users_in_db: Sequence[UserModel] = await get_users()
    #         assert compare_dicts_and_db_models(users_in_db, expected_result, UserDB)
    #
    # @pytest.mark.usefixtures('setup_users')
    # async def test_delete_all(
    #         self,
    #         transaction_session: AsyncSession,
    #         get_users: AsyncFunc,
    # ) -> None:
    #     sql_rep = self.__get_sql_rep(transaction_session)
    #     await sql_rep.delete_all()
    #     await transaction_session.flush()
    #     users_in_db: Sequence[UserModel] = await get_users()
    #     assert users_in_db == []
