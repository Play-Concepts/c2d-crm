"""
This file tests all Merchant routes
All of these routes require a merchant user
TODO: Inject Merchant Dependency
"""
import uuid
from typing import Tuple

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
from app.db.repositories.scan_transactions import ScanTransactionsRepository
from app.models.core import IDModelMixin
from app.models.customer import CustomerNew
from app.models.data_pass import InvalidDataPass
from app.models.merchant import MerchantEmailView
from app.models.scan_transaction import ScanRequest, ScanResult
from app.models.user import UserCreate
from app.tests.helpers.data_creator import (create_data_pass,
                                            create_data_source,
                                            create_data_verifier)
from app.tests.helpers.data_generator import (
    create_new_customer, create_new_data_pass_data,
    create_valid_data_pass_source_data, create_valid_data_pass_verifier_data,
    supplier_email)

pytestmark = pytest.mark.asyncio


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
    return create_new_data_pass_data("active", None)


@pytest.fixture
def test_data_pass_id() -> uuid.UUID:
    return uuid.uuid4()


class TestDataPass:
    data_pass_id: IDModelMixin


@pytest.fixture(scope="class")
def test_data_pass():
    return TestDataPass()


class TestMerchantRoutes:
    @pytest.mark.parametrize(
        "route_name, route_path, include_data_pass_id",
        [
            ("merchant:barcode_verify", "/api/merchant/{}/barcode/verify", True),
            (
                "merchant:scan_transactions_count",
                "/api/merchant/{}/scan_transactions_count",
                True,
            ),
        ],
    )
    async def test_merchant_routes_exists(
        self,
        app: FastAPI,
        client: AsyncClient,
        route_name: str,
        route_path: str,
        include_data_pass_id: bool,
        test_data_pass_id: uuid.UUID,
    ) -> None:
        if include_data_pass_id:
            assert app.url_path_for(
                route_name, data_pass_id=str(test_data_pass_id)
            ) == route_path.format(str(test_data_pass_id))
        else:
            assert app.url_path_for(route_name) == route_path

    async def test_merchant_barcode_verify_route(
        self,
        app: FastAPI,
        client: AsyncClient,
        customers_repository: CustomersRepository,
        data_passes_repository: DataPassesRepository,
        data_pass_sources_repository: DataPassSourcesRepository,
        data_pass_verifiers_repository: DataPassVerifiersRepository,
        scan_transactions_repository: ScanTransactionsRepository,
        user_merchant: Tuple[CreateUserProtocol, MerchantEmailView],
        valid_data_pass_source_data: dict,
        valid_data_pass_verifier_data: dict,
        valid_data_pass_data: dict,
        valid_customer: CustomerNew,
        test_data_pass: TestDataPass,
    ) -> None:
        from app.routes.merchant_route import verify_barcode

        # Setup
        _data_source = await create_data_source(
            valid_data_pass_source_data, data_pass_sources_repository
        )
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

        valid_customer.data_pass_id = valid_data_pass.id
        test_customer = await customers_repository.create_customer(
            new_customer=valid_customer
        )

        user, _ = user_merchant

        barcode = "{}:{}".format(test_customer.id, valid_data_pass.id)
        verify = await verify_barcode(
            None,
            valid_data_pass.id,
            ScanRequest(barcode=barcode),
            customers_repository,
            scan_transactions_repository,
            data_passes_repository,
            user,
        )
        assert isinstance(verify, ScanResult)
        assert verify.verified is True
        assert verify.message == ""

        invalid_data_pass_barcode = "{}:{}".format(test_customer.id, uuid.uuid4())
        verify = await verify_barcode(
            None,
            valid_data_pass.id,
            ScanRequest(barcode=invalid_data_pass_barcode),
            customers_repository,
            scan_transactions_repository,
            data_passes_repository,
            user,
        )
        assert isinstance(verify, InvalidDataPass)

        invalid_barcode = random_string(36)
        verify = await verify_barcode(
            None,
            valid_data_pass.id,
            ScanRequest(barcode=invalid_barcode),
            customers_repository,
            scan_transactions_repository,
            data_passes_repository,
            user,
        )
        assert isinstance(verify, InvalidDataPass)

    async def test_cleanup(
        self,
        app: FastAPI,
        client: AsyncClient,
        customers_repository: CustomersRepository,
        data_passes_repository: DataPassesRepository,
        test_data_pass: TestDataPass,
    ):
        await customers_repository.db.execute("TRUNCATE TABLE customers CASCADE;")
        cleanup_sql = """
            DELETE FROM data_passes WHERE id = :data_pass_id;
        """
        await data_passes_repository.db.fetch_one(
            query=cleanup_sql, values={"data_pass_id": test_data_pass.data_pass_id.id}
        )
        assert True
