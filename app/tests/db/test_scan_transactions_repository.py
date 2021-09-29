from datetime import datetime
from typing import Tuple

import pytest
from dateutil.relativedelta import relativedelta
from fastapi import FastAPI
from fastapi_users.user import CreateUserProtocol
from httpx import AsyncClient

from app.apis.utils.random import random_string
from app.core import global_state
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.data_pass_sources import DataPassSourcesRepository
from app.db.repositories.data_pass_verifiers import DataPassVerifiersRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.db.repositories.scan_transactions import ScanTransactionsRepository
from app.models.core import IDModelMixin
from app.models.customer import CustomerNew, CustomerView
from app.models.customer import StatusType as CustomerStatusType
from app.models.merchant import MerchantEmailView
from app.models.scan_transaction import (ScanTransactionBasicView,
                                         ScanTransactionCounts,
                                         ScanTransactionNew,
                                         ScanTransactionNewTest)
from app.models.user import UserCreate
from app.tests.helpers.data_creator import (create_data_pass,
                                            create_data_source,
                                            create_data_source_data_table,
                                            create_data_verifier)
from app.tests.helpers.data_generator import (
    create_new_customer, create_new_data_pass_data,
    create_valid_data_pass_source_data, create_valid_data_pass_verifier_data,
    supplier_email)

pytestmark = pytest.mark.asyncio


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
def valid_data_pass_test_data() -> dict:
    return create_new_data_pass_data("active")


@pytest.fixture(scope="class")
def customer_test_data() -> CustomerNew:
    return create_new_customer()


class TestCustomer:
    customer: CustomerView


@pytest.fixture(scope="class")
def test_customer():
    return TestCustomer()


class TestDataPass:
    data_pass_id: IDModelMixin


@pytest.fixture(scope="class")
def test_data_pass():
    return TestDataPass()


class TestDataTable:
    data_table: str


@pytest.fixture(scope="class")
def test_data_table():
    return TestDataTable()


@pytest.fixture(scope="class")
def test_pda_url():
    return "test.hubat.net"


class TestScanTransactionsRepository:
    async def test_create_scan_transaction(
        self,
        app: FastAPI,
        client: AsyncClient,
        customers_repository: CustomersRepository,
        customer_test_data: CustomerNew,
        test_customer: TestCustomer,
        data_passes_repository: DataPassesRepository,
        data_pass_sources_repository: DataPassSourcesRepository,
        data_pass_verifiers_repository: DataPassVerifiersRepository,
        valid_data_pass_source_data: dict,
        valid_data_pass_verifier_data: dict,
        valid_data_pass_test_data: dict,
        test_data_pass: TestDataPass,
        test_pda_url: str,
        test_data_table: TestDataTable,
        scan_transactions_repository: ScanTransactionsRepository,
        user_merchant: Tuple[CreateUserProtocol, MerchantEmailView],
    ):
        _data_source = await create_data_source(
            valid_data_pass_source_data, data_pass_sources_repository
        )
        _data_table = valid_data_pass_source_data["data_table"]
        await create_data_source_data_table(_data_table, data_pass_sources_repository)
        test_data_table.data_table = _data_table

        _data_verifier = await create_data_verifier(
            valid_data_pass_verifier_data, data_pass_verifiers_repository
        )
        valid_data_pass = await create_data_pass(
            _data_source.id,
            _data_verifier.id,
            valid_data_pass_test_data,
            data_passes_repository,
        )
        test_data_pass.data_pass_id = valid_data_pass

        customer_test_data.pda_url = test_pda_url
        customer_test_data.status = CustomerStatusType.claimed
        created_customer = await customers_repository.create_customer(
            new_customer=customer_test_data, data_table=_data_table
        )

        test_customer.customer = created_customer

        user, _ = user_merchant

        scan_transaction_new = ScanTransactionNew(
            customer_id=created_customer.id,
            user_id=user.id,
            data_pass_id=valid_data_pass.id,
            data_pass_verified_valid=True,
            data_pass_expired=False,
        )
        created_scan_transaction = (
            await scan_transactions_repository.create_scan_transaction(
                scan_transaction=scan_transaction_new,
            )
        )
        assert created_scan_transaction is not None
        assert isinstance(created_scan_transaction, ScanTransactionBasicView)

        # cleanup so the created transaction doesn't affect the remaining tests
        await scan_transactions_repository.db.execute(
            "DELETE FROM scan_transactions where id = '{}'".format(
                created_scan_transaction.id
            )
        )

    async def test_get_scan_trans_count_with_interval_n_days(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_customer: TestCustomer,
        test_data_pass: TestDataPass,
        scan_transactions_repository: ScanTransactionsRepository,
        user_merchant: Tuple[CreateUserProtocol, MerchantEmailView],
    ):
        user, _ = user_merchant

        for i in range(1, 10):
            scan_transaction_new = ScanTransactionNewTest(
                customer_id=test_customer.customer.id,
                user_id=user.id,
                data_pass_id=test_data_pass.data_pass_id.id,
                data_pass_verified_valid=True,
                data_pass_expired=False,
                created_at=(datetime.now() - relativedelta(days=i)).replace(
                    hour=0, minute=0, second=0, microsecond=0
                ),
            )
            await scan_transactions_repository.create_scan_transaction(
                scan_transaction=scan_transaction_new,
            )

        scan_transactions_count = await scan_transactions_repository.get_scan_trans_count_with_interval_n_days(
            interval_days=3,
            user_id=user.id,
            data_pass_id=test_data_pass.data_pass_id.id,
        )
        assert scan_transactions_count is not None
        assert isinstance(scan_transactions_count, ScanTransactionCounts)
        assert scan_transactions_count.interval_1.total == 3
        assert scan_transactions_count.interval_1.valid == 3
        assert scan_transactions_count.interval_1.fails == 0
        assert scan_transactions_count.interval_2.total == 3
        assert scan_transactions_count.interval_2.valid == 3
        assert scan_transactions_count.interval_2.fails == 0
        assert scan_transactions_count.interval_3.total == 3
        assert scan_transactions_count.interval_3.valid == 3
        assert scan_transactions_count.interval_3.fails == 0

    async def test_get_customers_scan_transactions_count_with_interval_n_days(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_data_pass: TestDataPass,
        scan_transactions_repository: ScanTransactionsRepository,
        user_merchant: Tuple[CreateUserProtocol, MerchantEmailView],
        test_pda_url: str,
        test_data_table: TestDataTable,
    ):
        user, _ = user_merchant

        for i in range(1, 10):
            invalid_scan_transaction_new = ScanTransactionNewTest(
                customer_id=None,
                user_id=user.id,
                data_pass_id=test_data_pass.data_pass_id.id,
                data_pass_verified_valid=False,
                data_pass_expired=False,
                created_at=datetime.now() - relativedelta(days=i),
            )
            await scan_transactions_repository.create_scan_transaction(
                scan_transaction=invalid_scan_transaction_new,
            )

        scan_transactions_count = await scan_transactions_repository.get_customer_scan_trans_count_with_interval_n_days(
            interval_days=3,
            pda_url=test_pda_url,
            data_pass_id=test_data_pass.data_pass_id.id,
            data_table=test_data_table.data_table,
        )
        assert scan_transactions_count is not None
        assert isinstance(scan_transactions_count, ScanTransactionCounts)
        assert scan_transactions_count.interval_1.total == 3
        assert scan_transactions_count.interval_1.valid == 3
        assert scan_transactions_count.interval_1.fails == 0
        assert scan_transactions_count.interval_2.total == 3
        assert scan_transactions_count.interval_2.valid == 3
        assert scan_transactions_count.interval_2.fails == 0
        assert scan_transactions_count.interval_3.total == 3
        assert scan_transactions_count.interval_3.valid == 3
        assert scan_transactions_count.interval_3.fails == 0

    async def test_cleanup(
        self,
        app: FastAPI,
        client: AsyncClient,
        data_passes_repository: DataPassesRepository,
        test_data_pass: TestDataPass,
        test_data_table: TestDataTable,
    ):
        await data_passes_repository.db.execute(
            "TRUNCATE TABLE scan_transactions CASCADE;"
        )
        await data_passes_repository.db.execute("TRUNCATE TABLE {data_table} CASCADE;".format(data_table=test_data_table.data_table))
        cleanup_sql = """
            DELETE FROM data_passes WHERE id = :data_pass_id;
        """
        await data_passes_repository.db.fetch_one(
            query=cleanup_sql, values={"data_pass_id": test_data_pass.data_pass_id.id}
        )
        assert True
