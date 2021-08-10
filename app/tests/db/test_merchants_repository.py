import uuid
from typing import List

import pytest
from faker import Faker
from faker.providers import company, internet, misc
from fastapi import FastAPI
from httpx import AsyncClient

from app.apis.utils.random import random_string
from app.core import global_state
from app.db.repositories.merchants import MerchantsRepository
from app.db.repositories.users import UsersRepository
from app.models.merchant import MerchantNew, MerchantView
from app.models.user import UserCreate, UserView
from app.tests.helpers.data_generator import create_new_merchant

pytestmark = pytest.mark.asyncio


NUMBER_OF_TEST_RECORDS = 5


@pytest.fixture
def new_merchants_test_data() -> List[MerchantNew]:
    return [create_new_merchant() for i in range(NUMBER_OF_TEST_RECORDS)]


class TestMerchantsRepository:
    async def test_create_merchant(
        self,
        app: FastAPI,
        client: AsyncClient,
        merchants_repository: MerchantsRepository,
        new_merchants_test_data: List[MerchantNew],
    ):
        print(new_merchants_test_data)
        test_new_merchant = new_merchants_test_data[0]
        created_merchant = await merchants_repository.create_merchant(
            new_merchant=test_new_merchant
        )
        assert created_merchant is not None
        assert isinstance(created_merchant, MerchantView)
        assert isinstance(created_merchant.id, uuid.UUID)

    def test_get_merchants_email_list(self):
        assert True

    def test_update_welcome_email_sent(self):
        assert True

    def test_get_merchant_by_email(self):
        assert True
