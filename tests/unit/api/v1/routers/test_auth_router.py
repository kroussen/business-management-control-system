from typing import Any

import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient

from sqlalchemy import text

from tests.fixtures import test_cases
from tests.utils import prepare_payload
from utils.unit_of_work import transaction_mode

# TODO удалить
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class TestAuthRouter:

    @staticmethod
    @pytest.mark.parametrize(
        ('url', 'json', 'headers', 'expected_status_code', 'expected_payload', 'expectation'),
        test_cases.auth.PARAMS_TEST_CHECK_ACCOUNT_ROUTER,
    )
    @pytest.mark.skip
    async def test_get_check_account(
            url: str,
            json: dict,
            headers: dict,
            expected_status_code: int,
            expected_payload: dict,
            expectation: Any,
            async_client: AsyncClient,
    ) -> None:
        with expectation:
            response = await async_client.get(url, headers=headers)
            assert response.status_code == expected_status_code
            assert response.json() == expected_payload

    @staticmethod
    @pytest.mark.usefixtures('setup_invites')
    @pytest.mark.parametrize(
        ('url', 'json', 'headers', 'expected_status_code', 'expected_payload', 'expectation'),
        test_cases.auth.PARAMS_TEST_SIGN_UP_ROUTER,
    )
    async def test_post_sign_up(
            url: str,
            json: dict,
            headers: dict,
            expected_status_code: int,
            expected_payload: dict,
            expectation: Any,
            async_client: AsyncClient,
    ) -> None:
        with expectation:
            response = await async_client.post(url, json=json, headers=headers)
            assert response.status_code == expected_status_code
            assert response.json() == expected_payload
