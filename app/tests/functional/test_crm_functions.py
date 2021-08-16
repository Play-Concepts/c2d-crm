import uuid

import pytest
from fastapi import FastAPI, Response, status
from httpx import AsyncClient

from app.db.repositories.customers import CustomersRepository
from app.models.customer import CustomerNew, CustomerView
from app.tests.helpers.data_generator import create_new_customer

pytestmark = pytest.mark.asyncio


class TestCustomer:
    customer: CustomerView


@pytest.fixture(scope="class")
def test_customer():
    return create_new_customer()


@pytest.fixture
def test_response():
    return Response()


class TestCrmFunctions:
    @pytest.mark.xfail(
        reason="IGNORING: no additional codes in function to test. "
        "Tested by ../db/test_customers_repository::get_customers"
    )
    async def test_fn_list_customers(
        self,
        app: FastAPI,
        client: AsyncClient,
    ) -> None:
        assert False

    @pytest.mark.xfail(reason="TODO")
    async def test_fn_get_customer(
        self,
        app: FastAPI,
        client: AsyncClient,
        customers_repository: CustomersRepository,
        test_customer: CustomerNew,
        test_response: Response,
    ) -> None:
        created_customer = await customers_repository.create_customer(
            new_customer=test_customer
        )

        assert created_customer is not None
        assert isinstance(created_customer, CustomerView)

        from app.apis.crm.mainmod import fn_get_customer as fn_to_test

        customer = await fn_to_test(
            created_customer.id, customers_repository, test_response
        )
        assert test_response.status_code == status.HTTP_200_OK
        assert customer.id == created_customer.id

        customer = await fn_to_test(uuid.uuid4(), customers_repository, test_response)
        assert customer is None
        assert test_response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.xfail(reason="TODO")
    async def test_fn_customer_upload(
        self,
        app: FastAPI,
        client: AsyncClient,
    ) -> None:
        assert True

    @pytest.mark.xfail(reason="TODO")
    async def test_fn_merchant_upload(
        self,
        app: FastAPI,
        client: AsyncClient,
    ) -> None:
        assert True
