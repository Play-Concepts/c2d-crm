import uuid
from typing import List

import pytest
from databases import Database
from faker import Faker
from faker.providers import internet, lorem
from fastapi import FastAPI
from httpx import AsyncClient

from app.apis.merchant.mainmod import fn_verify_barcode
from app.apis.utils.random import random_string
from app.core import global_state
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.db.repositories.scan_transactions import ScanTransactionsRepository
from app.models.core import IDModelMixin
from app.models.customer import CustomerNew
from app.models.user import UserCreate
from app.tests.helpers.data_generator import (create_new_customer,
                                              create_new_merchant)

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


@pytest.fixture(scope="class")
def valid_data_pass_source_verifier_data() -> dict:
    return {
        "name": fake.first_name().lower() + "-" + fake.pystr_format("?????").lower(),
        "description": fake.sentence(),
        "logo_url": fake.image_url(),
        "is_data_source": True,
        "is_data_verifier": True,
    }


@pytest.fixture(scope="class")
def valid_data_pass_data() -> dict:
    return {
        "name": fake.first_name().lower() + "-" + fake.pystr_format("?????").lower(),
        "title": fake.sentence(),
        "description_for_merchants": fake.sentence(),
        "description_for_customers": fake.sentence(),
        "perks_url_for_merchants": fake.url(),
        "perks_url_for_customers": fake.url(),
        "currency_code": "USD",
        "price": 0,
        "status": "active",
    }


class TestMerchantFunctions:
    async def _get_current_valid_user_id(self, user, db: Database):
        user = await db.fetch_one(
            query="SELECT id FROM users WHERE email=:email",
            values={"email": user.email},
        )

        return IDModelMixin(**user)

    async def _create_data_source_and_verifier(
        self, data: dict, data_passes_repo: DataPassesRepository
    ):
        return await data_passes_repo.create_data_pass_source_(**data)

    async def _create_data_pass(
        self,
        data_pass_source_id: uuid.UUID,
        data: dict,
        data_passes_repo: DataPassesRepository,
    ):
        data_pass_data = data
        data_pass_data["data_pass_source_id"] = data_pass_source_id
        data_pass_data["data_pass_verifier_id"] = data_pass_source_id
        return await data_passes_repo.create_data_pass_(**data_pass_data)

    async def _barcode_tester(
        self,
        barcode: str,
        data_pass_id: uuid.UUID,
        user_id: uuid.UUID,
        customers_repo: CustomersRepository,
        scan_transactions_repo: ScanTransactionsRepository,
    ) -> List:
        return await fn_verify_barcode(
            barcode,
            data_pass_id,
            user_id,
            customers_repo,
            scan_transactions_repo,
            raw=True,
        )

    async def test_fn_verify_barcode(
        self,
        app: FastAPI,
        client: AsyncClient,
        customers_repository: CustomersRepository,
        scan_transactions_repository: ScanTransactionsRepository,
        data_passes_repository: DataPassesRepository,
        db: Database,
        valid_user,
        valid_data_pass_source_verifier_data: dict,
        valid_data_pass_data: dict,
        valid_customer: CustomerNew,
    ) -> None:

        test_user = await self._get_current_valid_user_id(valid_user, db)
        _data_source_and_verifier = await self._create_data_source_and_verifier(
            valid_data_pass_source_verifier_data, data_passes_repository
        )
        test_data_pass = await self._create_data_pass(
            _data_source_and_verifier.id, valid_data_pass_data, data_passes_repository
        )

        xbarcode_with_existing_data_pass_and_user_must_return_null_customer_id = (
            self._barcode_tester
        )
        (
            customer_id,
            barcode_customer_uuid,
            barcode_data_pass_uuid,
        ) = await xbarcode_with_existing_data_pass_and_user_must_return_null_customer_id(
            random_string(),
            test_data_pass.id,
            test_user.id,
            customers_repository,
            scan_transactions_repository,
        )
        assert customer_id is None
        assert barcode_customer_uuid is None
        assert barcode_data_pass_uuid is None

        xsplitbarcode_with_existing_data_pass_and_user_must_return_null_customer_id = (
            self._barcode_tester
        )
        (
            customer_id,
            barcode_customer_uuid,
            barcode_data_pass_uuid,
        ) = await xsplitbarcode_with_existing_data_pass_and_user_must_return_null_customer_id(
            random_string(10) + ":" + random_string(10),
            test_data_pass.id,
            test_user.id,
            customers_repository,
            scan_transactions_repository,
        )
        assert customer_id is None
        assert barcode_customer_uuid is None
        assert barcode_data_pass_uuid is None

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
        ) = await barcode_with_customer_and_xdatapass_must_return_null_customer_id(
            str(test_customer.id) + ":" + random_string(10),
            test_data_pass.id,
            test_user.id,
            customers_repository,
            scan_transactions_repository,
        )
        assert customer_id is None
        assert barcode_customer_uuid is None
        assert barcode_data_pass_uuid is None

        fake_data_pass_id = uuid.uuid4()
        barcode_with_customer_and_nondatapass_must_return_null_customer_id = (
            self._barcode_tester
        )
        (
            customer_id,
            barcode_customer_uuid,
            barcode_data_pass_uuid,
        ) = await barcode_with_customer_and_nondatapass_must_return_null_customer_id(
            str(test_customer.id) + ":" + str(fake_data_pass_id),
            test_data_pass.id,
            test_user.id,
            customers_repository,
            scan_transactions_repository,
        )
        assert customer_id is None
        assert barcode_customer_uuid == test_customer.id
        assert barcode_data_pass_uuid == fake_data_pass_id

        valid_data_pass_data_2 = valid_data_pass_data
        valid_data_pass_data_2["name"] = (
            fake.first_name().lower() + "-" + fake.pystr_format("?????").lower()
        )

        test_data_pass_2 = await self._create_data_pass(
            _data_source_and_verifier.id, valid_data_pass_data_2, data_passes_repository
        )
        barcode_with_customer_and_wrong_datapass_must_return_null_customer_id = (
            self._barcode_tester
        )
        (
            customer_id,
            barcode_customer_uuid,
            barcode_data_pass_uuid,
        ) = await barcode_with_customer_and_wrong_datapass_must_return_null_customer_id(
            str(test_customer.id) + ":" + str(test_data_pass_2.id),
            test_data_pass.id,
            test_user.id,
            customers_repository,
            scan_transactions_repository,
        )
        assert customer_id is None
        assert barcode_customer_uuid == test_customer.id
        assert barcode_data_pass_uuid == test_data_pass_2.id

        barcode_with_correct_customer_and_datapass_must_return_customer_id = (
            self._barcode_tester
        )
        (
            customer_id,
            barcode_customer_uuid,
            barcode_data_pass_uuid,
        ) = await barcode_with_correct_customer_and_datapass_must_return_customer_id(
            str(test_customer.id) + ":" + str(test_data_pass.id),
            test_data_pass.id,
            test_user.id,
            customers_repository,
            scan_transactions_repository,
        )
        assert customer_id == test_customer.id
        assert barcode_customer_uuid == test_customer.id
        assert barcode_data_pass_uuid == test_data_pass.id

    @pytest.mark.xfail(reason="TODO")
    async def test_fn_get_scan_transactions_count(
        self,
        app: FastAPI,
        client: AsyncClient,
    ) -> None:
        assert True
