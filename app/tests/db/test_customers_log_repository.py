import random
from datetime import datetime
from typing import List

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.db.repositories.customers_log import CustomersLogRepository
from app.models.core import BooleanResponse
from app.models.customer_log import CustomerLogNew, CustomerLogNewResponse
from app.tests.helpers.data_generator import (create_new_customer_log,
                                              fake_hostname)

pytestmark = pytest.mark.asyncio


NUMBER_OF_TEST_RECORDS = 5


@pytest.fixture(scope="class")
def new_customers_log_test_data() -> List[CustomerLogNew]:
    return [create_new_customer_log() for _ in range(NUMBER_OF_TEST_RECORDS)]


class TestCustomersLogRepository:
    async def test_log_event(
        self,
        app: FastAPI,
        client: AsyncClient,
        customers_log_repository: CustomersLogRepository,
        new_customers_log_test_data: List[CustomerLogNew],
    ):
        test_new_customer_log = new_customers_log_test_data[0]
        created_customer_log = await customers_log_repository.log_event(
            customer_log_new=test_new_customer_log
        )
        assert created_customer_log is not None
        assert isinstance(created_customer_log, CustomerLogNewResponse)
        assert created_customer_log.id is not None
        assert isinstance(created_customer_log.created_at, datetime)

        # Prep for the following tests

        for customer_log in new_customers_log_test_data[1:]:
            await customers_log_repository.log_event(customer_log_new=customer_log)
        assert True

    async def test_customer_exists(
        self,
        app: FastAPI,
        client: AsyncClient,
        customers_log_repository: CustomersLogRepository,
        new_customers_log_test_data: List[CustomerLogNew],
    ):
        existing_customer_log = random.choice(new_customers_log_test_data)
        customer_exists = await customers_log_repository.customer_exists(
            pda_url=existing_customer_log.pda_url
        )

        assert isinstance(customer_exists, BooleanResponse)
        assert customer_exists.value is False

        customer_not_exists = await customers_log_repository.customer_exists(
            pda_url=fake_hostname()
        )
        assert customer_not_exists.value is True
