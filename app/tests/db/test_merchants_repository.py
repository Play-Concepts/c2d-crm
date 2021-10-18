import random
from datetime import datetime
from typing import List

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.db.repositories.merchants import MerchantsRepository
from app.models.core import IDModelMixin
from app.models.merchant import MerchantEmailView, MerchantNew
from app.tests.helpers.data_generator import create_new_merchant

pytestmark = pytest.mark.asyncio


NUMBER_OF_TEST_RECORDS = 5


@pytest.fixture(scope="class")
def new_merchants_test_data() -> List[MerchantNew]:
    return [create_new_merchant() for _ in range(NUMBER_OF_TEST_RECORDS)]


class TestMerchantsRepository:
    async def test_create_merchant(
        self,
        app: FastAPI,
        client: AsyncClient,
        merchants_repository: MerchantsRepository,
        new_merchants_test_data: List[MerchantNew],
    ):
        test_new_merchant = new_merchants_test_data[0]
        created_merchant = await merchants_repository.create_merchant(
            new_merchant=test_new_merchant
        )
        assert created_merchant is not None
        assert isinstance(created_merchant, IDModelMixin)
        assert created_merchant.id is not None

        # Prep for the folloing tests
        for merchant in new_merchants_test_data[1:]:
            await merchants_repository.create_merchant(new_merchant=merchant)
        assert True

    async def test_get_merchants_email_list(
        self,
        app: FastAPI,
        client: AsyncClient,
        merchants_repository: MerchantsRepository,
    ):
        merchants_email_list = await merchants_repository.get_merchants_email_list()

        # +1 for conftest.user_merchant fixture
        assert len(merchants_email_list) == NUMBER_OF_TEST_RECORDS
        assert isinstance(random.choice(merchants_email_list), MerchantEmailView)

    async def test_update_welcome_email_sent(
        self,
        app: FastAPI,
        client: AsyncClient,
        merchants_repository: MerchantsRepository,
    ):
        merchants_email_list = await merchants_repository.get_merchants_email_list()
        merchant = random.choice(merchants_email_list)
        updated_merchant = await merchants_repository.update_welcome_email_sent(
            merchant_id=merchant.id
        )
        assert updated_merchant is not None
        assert isinstance(updated_merchant.welcome_email_sent, datetime)
        assert updated_merchant.id == merchant.id

    async def test_get_merchant_by_email(
        self,
        app: FastAPI,
        client: AsyncClient,
        merchants_repository: MerchantsRepository,
        new_merchants_test_data: List[MerchantNew],
    ):
        test_merchant = random.choice(new_merchants_test_data)
        merchant = await merchants_repository.get_merchant_by_email(
            email=test_merchant.email
        )
        assert merchant is not None
        assert isinstance(merchant, MerchantEmailView)
        assert merchant.email == test_merchant.email
