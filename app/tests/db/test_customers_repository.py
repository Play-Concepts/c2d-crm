import random
from typing import List

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.db.repositories.customers import CustomersRepository
from app.models.customer import CustomerBasicView, CustomerNew, CustomerView
from app.tests.helpers.data_generator import create_new_customer

pytestmark = pytest.mark.asyncio


NUMBER_OF_TEST_RECORDS = 5


@pytest.fixture(scope="class")
def new_customers_test_data() -> List[CustomerNew]:
    return [create_new_customer() for _ in range(NUMBER_OF_TEST_RECORDS)]


class TestCustomer:
    customer: CustomerView


@pytest.fixture(scope="class")
def test_customer():
    return TestCustomer()


class TestCustomersRepository:
    async def test_create_customer(
        self,
        app: FastAPI,
        client: AsyncClient,
        customers_repository: CustomersRepository,
        new_customers_test_data: List[CustomerNew],
        test_customer: TestCustomer,
    ):
        test_new_customer = new_customers_test_data[0]
        created_customer = await customers_repository.create_customer(
            new_customer=test_new_customer
        )
        assert created_customer is not None
        assert isinstance(created_customer, CustomerView)
        assert created_customer.id is not None

        # Prep for the folloing tests
        test_customer.customer = created_customer

        for customer in new_customers_test_data[1:]:
            await customers_repository.create_customer(new_customer=customer)
        assert True

    async def test_get_customers(
        self,
        app: FastAPI,
        client: AsyncClient,
        customers_repository: CustomersRepository,
    ):
        offset, limit = 3, 2
        customers = await customers_repository.get_customers(offset=offset, limit=limit)
        assert len(customers) == 2
        assert isinstance(random.choice(customers), CustomerView)

    async def test_get_customer(
        self,
        app: FastAPI,
        client: AsyncClient,
        customers_repository: CustomersRepository,
        test_customer: TestCustomer,
    ):
        test_target = test_customer.customer
        customer = await customers_repository.get_customer(customer_id=test_target.id)
        assert customer is not None
        assert isinstance(customer, CustomerView)
        assert customer.id == test_target.id

    async def test_get_customer_basic(
        self,
        app: FastAPI,
        client: AsyncClient,
        customers_repository: CustomersRepository,
        new_customers_test_data: List[CustomerNew],
    ):
        test_customer = random.choice(new_customers_test_data)
        customer = await customers_repository.get_customer_basic(
            pda_url=test_customer.pda_url,
        )
        assert customer is not None
        assert isinstance(customer, CustomerBasicView)
        assert customer.id is not None
