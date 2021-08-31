import random
from typing import List

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.apis.utils.random import random_string
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

        # Prep for the following tests
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

    async def test_search_customers(
        self,
        app: FastAPI,
        client: AsyncClient,
        customers_repository: CustomersRepository,
        new_customers_test_data: List[CustomerNew],
    ):
        def random_pad(value: str) -> str:
            return value.rjust(random.randint(0, 10)).ljust(random.randint(0, 10))

        def is_empty(list) -> bool:
            return len(list) == 0

        test_customer_data = random.choice(new_customers_test_data).data
        test_last_name = test_customer_data["person"]["profile"]["last_name"]
        test_email = test_customer_data["person"]["contact"]["email"]
        test_address = test_customer_data["person"]["address"]["address_line_1"]

        customer = await customers_repository.search_customers(
            last_name=test_last_name,
            email=test_email,
            address=test_address,
        )
        assert not is_empty(customer)

        invalid_last_name_customer = await customers_repository.search_customers(
            last_name=random.choice([random_string(), ""]),
            email=test_email,
            address=test_address,
        )
        assert is_empty(invalid_last_name_customer)

        invalid_email_customer = await customers_repository.search_customers(
            last_name=test_last_name,
            email=random.choice([random_string(), ""]),
            address=test_address,
        )
        assert is_empty(invalid_email_customer)

        invalid_address_customer = await customers_repository.search_customers(
            last_name=test_last_name,
            email=test_email,
            address=random.choice([random_string(), ""]),
        )
        assert is_empty(invalid_address_customer)

        trimmed_last_name_customer = await customers_repository.search_customers(
            last_name=random_pad(test_last_name),
            email=test_email,
            address=test_address,
        )
        assert not is_empty(trimmed_last_name_customer)

        trimmed_email_customer = await customers_repository.search_customers(
            last_name=test_last_name,
            email=random_pad(test_email),
            address=test_address,
        )
        assert not is_empty(trimmed_email_customer)

        trimmed_address_customer = await customers_repository.search_customers(
            last_name=test_last_name,
            email=test_email,
            address=random_pad(test_address),
        )
        assert not is_empty(trimmed_address_customer)
