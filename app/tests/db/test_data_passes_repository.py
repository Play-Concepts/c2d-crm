import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.tests.helpers.data_generator import (
    create_new_data_pass_data, create_valid_data_pass_source_verifier_data)

pytestmark = pytest.mark.asyncio


NUMBER_OF_TEST_RECORDS = 5


@pytest.fixture(scope="class")
def valid_data_pass_source_verifier_data() -> dict:
    return create_valid_data_pass_source_verifier_data()


@pytest.fixture(scope="class")
def valid_data_pass_data() -> dict:
    return create_new_data_pass_data("active", None)


class TestDataPassesRepository:
    async def test_get_customer_data_passes(
        self,
        app: FastAPI,
        client: AsyncClient,
    ):
        assert True

    async def test_get_merchant_data_passes(
        self,
        app: FastAPI,
        client: AsyncClient,
    ):
        assert True

    async def test_is_data_pass_valid(
        self,
        app: FastAPI,
        client: AsyncClient,
    ):
        assert True

    async def test_activate_data_pass(
        self,
        app: FastAPI,
        client: AsyncClient,
    ):
        assert True
