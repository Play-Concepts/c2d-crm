import uuid

import pytest
from fastapi import FastAPI, Response, UploadFile, status
from httpx import AsyncClient

from app.db.repositories.customers import CustomersRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.db.repositories.merchants import MerchantsRepository
from app.models.core import CreatedCount, IDModelMixin, NotFound
from app.models.customer import CustomerNew, CustomerView
from app.tests.helpers.data_creator import (create_data_pass,
                                            create_data_source_and_verifier)
from app.tests.helpers.data_generator import (
    create_new_customer, create_new_data_pass_data,
    create_valid_data_pass_source_verifier_data)

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="class")
def valid_data_pass_source_verifier_data() -> dict:
    return create_valid_data_pass_source_verifier_data()


@pytest.fixture(scope="class")
def valid_data_pass_test_data() -> dict:
    return create_new_data_pass_data("active", None)


@pytest.fixture(scope="class")
def test_customer():
    return create_new_customer()


class TestDataPass:
    data_pass_id: IDModelMixin


@pytest.fixture(scope="class")
def test_data_pass():
    return TestDataPass()


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

    async def test_fn_get_customer(
        self,
        app: FastAPI,
        client: AsyncClient,
        customers_repository: CustomersRepository,
        test_customer: CustomerNew,
        test_response: Response,
        data_passes_repository: DataPassesRepository,
        valid_data_pass_source_verifier_data: dict,
        valid_data_pass_test_data: dict,
        test_data_pass: TestDataPass,
    ) -> None:
        _data_source_and_verifier = await create_data_source_and_verifier(
            valid_data_pass_source_verifier_data, data_passes_repository
        )
        valid_data_pass = await create_data_pass(
            _data_source_and_verifier.id,
            valid_data_pass_test_data,
            data_passes_repository,
        )
        test_data_pass.data_pass_id = valid_data_pass

        test_customer.data_pass_id = valid_data_pass.id
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
        assert isinstance(customer, NotFound)
        assert test_response.status_code == status.HTTP_404_NOT_FOUND

    async def test_fn_customer_upload(
        self,
        app: FastAPI,
        client: AsyncClient,
        customers_repository: CustomersRepository,
        customers_test_file: UploadFile,
        customers_test_file_records_number: int,
        data_passes_repository: DataPassesRepository,
        test_data_pass: TestDataPass,
    ) -> None:
        from app.apis.crm.mainmod import fn_customer_upload as fn_to_test

        res_count = await fn_to_test(
            test_data_pass.data_pass_id.id,
            data_passes_repository,
            customers_test_file,
            customers_repository,
        )
        assert isinstance(res_count, CreatedCount)
        assert res_count.count == customers_test_file_records_number

    async def test_fn_merchant_upload(
        self,
        app: FastAPI,
        client: AsyncClient,
        merchants_repository: MerchantsRepository,
        merchants_test_file: UploadFile,
        merchants_test_file_records_number: int,
    ) -> None:
        from app.apis.crm.mainmod import fn_merchant_upload as fn_to_test

        res_count = await fn_to_test(merchants_test_file, merchants_repository)
        assert isinstance(res_count, CreatedCount)
        assert res_count.count == merchants_test_file_records_number

    async def test_cleanup(
        self,
        app: FastAPI,
        client: AsyncClient,
        customers_repository: CustomersRepository,
        data_passes_repository: DataPassesRepository,
        test_data_pass: TestDataPass,
    ):
        await data_passes_repository.db.execute("TRUNCATE TABLE customers CASCADE;")
        cleanup_sql = """
            DELETE FROM data_passes WHERE id = :data_pass_id;
        """
        await data_passes_repository.db.fetch_one(
            query=cleanup_sql, values={"data_pass_id": test_data_pass.data_pass_id.id}
        )
        assert True
