import uuid
from datetime import datetime, timedelta
from typing import List

import pytest
from databases import Database
from faker import Faker
from faker.providers import internet, lorem
from fastapi import FastAPI
from fastapi_users.user import CreateUserProtocol
from httpx import AsyncClient

from app.apis.merchant.mainmod import fn_verify_barcode
from app.apis.utils.random import random_string
from app.core import global_state
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.data_pass_sources import DataPassSourcesRepository
from app.db.repositories.data_pass_verifiers import DataPassVerifiersRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.db.repositories.scan_transactions import ScanTransactionsRepository
from app.models.core import IDModelMixin
from app.models.customer import CustomerNew
from app.models.user import UserCreate
from app.tests.helpers.data_creator import (create_data_pass,
                                            create_data_source,
                                            create_data_verifier)
from app.tests.helpers.data_generator import (
    create_new_customer, create_new_data_pass_data, create_new_merchant,
    create_valid_data_pass_source_data, create_valid_data_pass_verifier_data,
    supplier_email)

pytestmark = pytest.mark.asyncio

fake = Faker()
fake.add_provider(internet)
fake.add_provider(lorem)


@pytest.fixture
async def valid_user():
    new_merchant = create_new_merchant()
    return await global_state.fastapi_users.create_user(
        UserCreate(
            email=new_merchant.email,
            password=random_string(),
            is_verified=True,
        )
    )


@pytest.fixture(scope="class")
def valid_customer() -> CustomerNew:
    return create_new_customer()


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
def expired_data_pass_test_data() -> dict:
    return create_new_data_pass_data("active", datetime.now() - timedelta(days=1))


class TestMerchantFunctions:
    async def _get_current_valid_user_id(self, user, db: Database):
        user = await db.fetch_one(
            query="SELECT id FROM users WHERE email=:email",
            values={"email": user.email},
        )

        return IDModelMixin(**user)

    async def _barcode_tester(
        self,
        barcode: str,
        data_pass_id: uuid.UUID,
        user_id: uuid.UUID,
        customers_repo: CustomersRepository,
        scan_transactions_repo: ScanTransactionsRepository,
        data_passes_repo: DataPassesRepository,
    ) -> List:
        return await fn_verify_barcode(
            barcode,
            data_pass_id,
            user_id,
            customers_repo,
            scan_transactions_repo,
            data_passes_repo,
            raw=True,
        )

    @pytest.mark.xfail(reason="TODO: TO-FIX PRIORITY - Broken due to removed CUSTOMERS")
    async def test_fn_verify_barcode(
        self,
        app: FastAPI,
        client: AsyncClient,
        customers_repository: CustomersRepository,
        scan_transactions_repository: ScanTransactionsRepository,
        data_passes_repository: DataPassesRepository,
        data_pass_sources_repository: DataPassSourcesRepository,
        data_pass_verifiers_repository: DataPassVerifiersRepository,
        db: Database,
        valid_user,
        valid_data_pass_source_data: dict,
        valid_data_pass_verifier_data: dict,
        valid_data_pass_data: dict,
        expired_data_pass_test_data: dict,
        valid_customer: CustomerNew,
    ) -> None:

        test_user = await self._get_current_valid_user_id(valid_user, db)
        _data_source = await create_data_source(
            valid_data_pass_source_data, data_pass_sources_repository
        )
        _data_verifier = await create_data_verifier(
            valid_data_pass_verifier_data, data_pass_verifiers_repository
        )
        test_data_pass = await create_data_pass(
            _data_source.id,
            _data_verifier.id,
            valid_data_pass_data,
            data_passes_repository,
        )

        xbarcode_with_existing_data_pass_and_user_must_return_null_customer_id = (
            self._barcode_tester
        )
        (
            customer_id,
            barcode_customer_uuid,
            barcode_data_pass_uuid,
            is_valid_data_pass,
        ) = await xbarcode_with_existing_data_pass_and_user_must_return_null_customer_id(
            random_string(),
            test_data_pass.id,
            test_user.id,
            customers_repository,
            scan_transactions_repository,
            data_passes_repository,
        )
        assert customer_id is None
        assert barcode_customer_uuid is None
        assert barcode_data_pass_uuid is None
        assert not is_valid_data_pass

        xsplitbarcode_with_existing_data_pass_and_user_must_return_null_customer_id = (
            self._barcode_tester
        )
        (
            customer_id,
            barcode_customer_uuid,
            barcode_data_pass_uuid,
            is_valid_data_pass,
        ) = await xsplitbarcode_with_existing_data_pass_and_user_must_return_null_customer_id(
            random_string(10) + ":" + random_string(10),
            test_data_pass.id,
            test_user.id,
            customers_repository,
            scan_transactions_repository,
            data_passes_repository,
        )
        assert customer_id is None
        assert barcode_customer_uuid is None
        assert barcode_data_pass_uuid is None
        assert not is_valid_data_pass

        valid_customer.data_pass_id = test_data_pass.id
        test_customer = await customers_repository.create_customer(
            new_customer=valid_customer
        )

        barcode_with_customer_and_xdatapass_must_return_null_customer_id = (
            self._barcode_tester
        )
        (
            customer_id,
            barcode_customer_uuid,
            barcode_data_pass_uuid,
            is_valid_data_pass,
        ) = await barcode_with_customer_and_xdatapass_must_return_null_customer_id(
            str(test_customer.id) + ":" + random_string(10),
            test_data_pass.id,
            test_user.id,
            customers_repository,
            scan_transactions_repository,
            data_passes_repository,
        )
        assert customer_id is None
        assert barcode_customer_uuid is None
        assert barcode_data_pass_uuid is None
        assert not is_valid_data_pass

        fake_data_pass_id = uuid.uuid4()
        barcode_with_customer_and_nondatapass_must_return_null_customer_id = (
            self._barcode_tester
        )
        (
            customer_id,
            barcode_customer_uuid,
            barcode_data_pass_uuid,
            is_valid_data_pass,
        ) = await barcode_with_customer_and_nondatapass_must_return_null_customer_id(
            str(test_customer.id) + ":" + str(fake_data_pass_id),
            test_data_pass.id,
            test_user.id,
            customers_repository,
            scan_transactions_repository,
            data_passes_repository,
        )
        assert customer_id is None
        assert barcode_customer_uuid == test_customer.id
        assert barcode_data_pass_uuid == fake_data_pass_id
        assert not is_valid_data_pass

        valid_data_pass_data_2 = valid_data_pass_data
        valid_data_pass_data_2["name"] = (
            fake.first_name().lower() + "-" + fake.pystr_format("?????").lower()
        )

        test_data_pass_2 = await create_data_pass(
            _data_source.id,
            _data_verifier.id,
            valid_data_pass_data_2,
            data_passes_repository,
        )
        barcode_with_customer_and_wrong_datapass_must_return_null_customer_id = (
            self._barcode_tester
        )
        (
            customer_id,
            barcode_customer_uuid,
            barcode_data_pass_uuid,
            is_valid_data_pass,
        ) = await barcode_with_customer_and_wrong_datapass_must_return_null_customer_id(
            str(test_customer.id) + ":" + str(test_data_pass_2.id),
            test_data_pass.id,
            test_user.id,
            customers_repository,
            scan_transactions_repository,
            data_passes_repository,
        )
        assert customer_id is None
        assert barcode_customer_uuid == test_customer.id
        assert barcode_data_pass_uuid == test_data_pass_2.id
        assert is_valid_data_pass

        barcode_with_correct_customer_and_datapass_must_return_customer_id = (
            self._barcode_tester
        )
        (
            customer_id,
            barcode_customer_uuid,
            barcode_data_pass_uuid,
            is_valid_data_pass,
        ) = await barcode_with_correct_customer_and_datapass_must_return_customer_id(
            str(test_customer.id) + ":" + str(test_data_pass.id),
            test_data_pass.id,
            test_user.id,
            customers_repository,
            scan_transactions_repository,
            data_passes_repository,
        )
        assert customer_id == test_customer.id
        assert barcode_customer_uuid == test_customer.id
        assert barcode_data_pass_uuid == test_data_pass.id
        assert is_valid_data_pass

        expired_data_pass = await create_data_pass(
            _data_source.id,
            _data_verifier.id,
            expired_data_pass_test_data,
            data_passes_repository,
        )
        barcode_with_correct_customer_and_expired_datapass_must_return_customer_id = (
            self._barcode_tester
        )
        (
            customer_id,
            barcode_customer_uuid,
            barcode_data_pass_uuid,
            is_valid_data_pass,
        ) = await barcode_with_correct_customer_and_expired_datapass_must_return_customer_id(
            str(test_customer.id) + ":" + str(expired_data_pass.id),
            expired_data_pass.id,
            test_user.id,
            customers_repository,
            scan_transactions_repository,
            data_passes_repository,
        )
        assert customer_id == test_customer.id
        assert barcode_customer_uuid == test_customer.id
        assert barcode_data_pass_uuid == expired_data_pass.id
        assert not is_valid_data_pass

    @pytest.mark.skip(reason="IGNORING: direct passthrough to db")
    async def test_fn_get_scan_transactions_count(
        self,
        app: FastAPI,
        client: AsyncClient,
    ) -> None:
        assert True
