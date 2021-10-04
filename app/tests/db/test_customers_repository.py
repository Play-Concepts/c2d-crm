import random
from typing import List

import pytest
from fastapi import FastAPI
from fastapi_users.user import CreateUserProtocol
from httpx import AsyncClient

from app.apis.utils.random import random_string
from app.core import global_state
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.data_pass_sources import DataPassSourcesRepository
from app.db.repositories.data_pass_verifiers import DataPassVerifiersRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.models.customer import CustomerNew, CustomerView
from app.models.user import UserCreate
from app.tests.helpers.data_creator import (create_data_pass,
                                            create_data_source,
                                            create_data_source_data_table,
                                            create_data_verifier)
from app.tests.helpers.data_generator import (
    create_new_customer, create_new_data_pass_data,
    create_valid_data_pass_source_data, create_valid_data_pass_verifier_data,
    supplier_email)
from app.tests.test_models import TestCustomer, TestDataPass, TestDataTable

pytestmark = pytest.mark.asyncio


NUMBER_OF_TEST_RECORDS = 5


@pytest.fixture
async def data_supplier_user() -> CreateUserProtocol:
    return await global_state.fastapi_users.create_user(
        UserCreate(
            email=supplier_email(),
            password=random_string(),
            is_verified=True,
            is_supplier=True,
        )
    )


@pytest.fixture
async def valid_data_pass_source_data(data_supplier_user: CreateUserProtocol) -> dict:
    return create_valid_data_pass_source_data(data_supplier_user.id)


@pytest.fixture(scope="class")
def valid_data_pass_verifier_data() -> dict:
    return create_valid_data_pass_verifier_data()


@pytest.fixture(scope="class")
def valid_data_pass_data() -> dict:
    return create_new_data_pass_data("active")


@pytest.fixture(scope="class")
def new_customers_test_data() -> List[CustomerNew]:
    return [create_new_customer() for _ in range(NUMBER_OF_TEST_RECORDS)]


@pytest.fixture(scope="class")
def test_customer():
    return TestCustomer()


@pytest.fixture(scope="class")
def test_data_pass():
    return TestDataPass()


@pytest.fixture(scope="class")
def test_data_table():
    return TestDataTable()


class TestCustomersRepository:
    async def test_create_customer(
        self,
        app: FastAPI,
        client: AsyncClient,
        customers_repository: CustomersRepository,
        new_customers_test_data: List[CustomerNew],
        test_customer: TestCustomer,
        data_passes_repository: DataPassesRepository,
        data_pass_sources_repository: DataPassSourcesRepository,
        data_pass_verifiers_repository: DataPassVerifiersRepository,
        valid_data_pass_source_data: dict,
        valid_data_pass_verifier_data: dict,
        valid_data_pass_data: dict,
        test_data_pass: TestDataPass,
        test_data_table: TestDataTable,
    ):
        # Setup
        _data_source = await create_data_source(
            valid_data_pass_source_data, data_pass_sources_repository
        )
        _data_table = valid_data_pass_source_data["data_table"]
        await create_data_source_data_table(_data_table, data_pass_sources_repository)
        test_data_table.data_table = _data_table
        test_data_table.search_sql = valid_data_pass_source_data["search_sql"]

        _data_verifier = await create_data_verifier(
            valid_data_pass_verifier_data, data_pass_verifiers_repository
        )
        valid_data_pass = await create_data_pass(
            _data_source.id,
            _data_verifier.id,
            valid_data_pass_data,
            data_passes_repository,
        )
        test_data_pass.data_pass_id = valid_data_pass

        test_new_customer = new_customers_test_data[0]
        created_customer = await customers_repository.create_customer(
            new_customer=test_new_customer,
            data_table=_data_table,
        )
        assert created_customer is not None
        assert isinstance(created_customer, CustomerView)
        assert created_customer.id is not None

        # Prep for the following tests
        test_customer.customer = created_customer

        for customer in new_customers_test_data[1:]:
            await customers_repository.create_customer(
                new_customer=customer,
                data_table=_data_table,
            )
        assert True

    async def test_get_customer(
        self,
        app: FastAPI,
        client: AsyncClient,
        customers_repository: CustomersRepository,
        test_customer: TestCustomer,
        test_data_table: TestDataTable,
    ):
        test_target = test_customer.customer
        _data_table = test_data_table.data_table
        customer = await customers_repository.get_customer(
            customer_id=test_target.id, data_table=_data_table
        )
        assert customer is not None
        assert isinstance(customer, CustomerView)
        assert customer.id == test_target.id

    async def test_search_customers(
        self,
        app: FastAPI,
        client: AsyncClient,
        customers_repository: CustomersRepository,
        new_customers_test_data: List[CustomerNew],
        test_data_table: TestDataTable,
    ):
        def random_pad(value: str) -> str:
            return value.rjust(random.randint(0, 10)).ljust(random.randint(0, 10))

        def is_empty(list) -> bool:
            return len(list) == 0

        _data_table = test_data_table.data_table
        _search_sql = test_data_table.search_sql
        test_customer_data = random.choice(new_customers_test_data).data
        test_last_name = test_customer_data["person"]["profile"]["last_name"]
        test_email = test_customer_data["person"]["contact"]["email"]
        test_address = test_customer_data["person"]["address"]["address_line_1"]

        customer = await customers_repository.search_customers(
            data_table=_data_table,
            search_sql=_search_sql,
            search_params={
                "last_name": test_last_name,
                "email": test_email,
                "address": test_address,
            },
        )
        assert not is_empty(customer)

        invalid_last_name_customer = await customers_repository.search_customers(
            data_table=_data_table,
            search_sql=_search_sql,
            search_params={
                "last_name": random.choice([random_string(), ""]),
                "email": test_email,
                "address": test_address,
            },
        )
        assert is_empty(invalid_last_name_customer)

        invalid_email_customer = await customers_repository.search_customers(
            data_table=_data_table,
            search_sql=_search_sql,
            search_params={
                "last_name": test_last_name,
                "email": random.choice([random_string(), ""]),
                "address": test_address,
            },
        )
        assert is_empty(invalid_email_customer)

        invalid_address_customer = await customers_repository.search_customers(
            data_table=_data_table,
            search_sql=_search_sql,
            search_params={
                "last_name": test_last_name,
                "email": test_email,
                "address": random.choice([random_string(), ""]),
            },
        )
        assert is_empty(invalid_address_customer)

        trimmed_last_name_customer = await customers_repository.search_customers(
            data_table=_data_table,
            search_sql=_search_sql,
            search_params={
                "last_name": random_pad(test_last_name),
                "email": test_email,
                "address": test_address,
            },
        )
        assert not is_empty(trimmed_last_name_customer)

        trimmed_email_customer = await customers_repository.search_customers(
            data_table=_data_table,
            search_sql=_search_sql,
            search_params={
                "last_name": test_last_name,
                "email": random_pad(test_email),
                "address": test_address,
            },
        )
        assert not is_empty(trimmed_email_customer)

        trimmed_address_customer = await customers_repository.search_customers(
            data_table=_data_table,
            search_sql=_search_sql,
            search_params={
                "last_name": test_last_name,
                "email": test_email,
                "address": random_pad(test_address),
            },
        )
        assert not is_empty(trimmed_address_customer)

    async def test_cleanup(
        self,
        app: FastAPI,
        client: AsyncClient,
        customers_repository: CustomersRepository,
        data_passes_repository: DataPassesRepository,
        test_data_pass: TestDataPass,
        test_data_table: TestDataTable,
    ):
        _data_table = test_data_table.data_table
        await customers_repository.db.execute("DROP TABLE {};".format(_data_table))
        cleanup_sql = """
            DELETE FROM data_passes WHERE id = :data_pass_id;
        """
        await data_passes_repository.db.fetch_one(
            query=cleanup_sql, values={"data_pass_id": test_data_pass.data_pass_id.id}
        )
        assert True
