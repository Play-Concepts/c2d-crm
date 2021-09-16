import uuid
from datetime import datetime, timedelta
from typing import List

import pytest
from fastapi import FastAPI
from fastapi_users.user import CreateUserProtocol
from httpx import AsyncClient

from app.apis.utils.random import random_string
from app.core import global_state
from app.db.repositories.data_pass_sources import DataPassSourcesRepository
from app.db.repositories.data_pass_verifiers import DataPassVerifiersRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.models.core import IDModelMixin
from app.models.user import UserCreate
from app.tests.helpers.data_creator import (create_data_pass,
                                            create_data_source,
                                            create_data_verifier)
from app.tests.helpers.data_generator import (
    create_new_data_pass_data, create_valid_data_pass_source_data,
    create_valid_data_pass_verifier_data, supplier_email)

pytestmark = pytest.mark.asyncio


NUMBER_OF_TEST_RECORDS = 5


class TestDataPassVerifier:
    data_pass_verifier: IDModelMixin


@pytest.fixture(scope="class")
def test_data_pass_verifier():
    return TestDataPassVerifier()


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
def valid_data_pass_test_data() -> List[dict]:
    return [
        create_new_data_pass_data("active", None) for _ in range(NUMBER_OF_TEST_RECORDS)
    ]


@pytest.fixture
def valid_data_pass_source_data_for_expiry_test(data_supplier_user: CreateUserProtocol) -> dict:
    return create_valid_data_pass_source_data(data_supplier_user.id)


@pytest.fixture(scope="class")
def non_expired_data_pass_test_data() -> dict:
    return create_new_data_pass_data("active", datetime.now() + timedelta(days=1))


@pytest.fixture(scope="class")
def expired_data_pass_test_data() -> dict:
    return create_new_data_pass_data("active", datetime.now() - timedelta(days=1))


class TestDataPassesRepository:
    async def test_get_customer_data_passes(
        self,
        app: FastAPI,
        client: AsyncClient,
        data_passes_repository: DataPassesRepository,
        data_pass_sources_repository: DataPassSourcesRepository,
        data_pass_verifiers_repository: DataPassVerifiersRepository,
        valid_data_pass_source_data: dict,
        valid_data_pass_verifier_data: dict,
        valid_data_pass_test_data: List[dict],
        test_data_pass_verifier: TestDataPassVerifier,
    ):
        await data_passes_repository.db.execute("TRUNCATE TABLE data_passes CASCADE;")

        _data_source = await create_data_source(
            valid_data_pass_source_data, data_pass_sources_repository
        )

        _data_verifier = await create_data_verifier(
            valid_data_pass_verifier_data, data_pass_verifiers_repository
        )
        for valid_data_pass_data in valid_data_pass_test_data:
            await create_data_pass(
                _data_source.id,
                _data_verifier.id,
                valid_data_pass_data,
                data_passes_repository,
            )
        test_data_pass_verifier.data_pass_verifier = _data_verifier

        data_passes = await data_passes_repository.get_customer_data_passes(pda_url="")
        assert len(data_passes) == NUMBER_OF_TEST_RECORDS

    async def test_get_merchant_data_passes(
        self,
        app: FastAPI,
        client: AsyncClient,
        data_passes_repository: DataPassesRepository,
    ):
        data_passes = await data_passes_repository.get_merchant_data_passes()
        assert len(data_passes) == NUMBER_OF_TEST_RECORDS

    async def test_is_data_pass_valid(
        self,
        app: FastAPI,
        client: AsyncClient,
        data_passes_repository: DataPassesRepository,
    ):
        valid_data_pass = await data_passes_repository.get_random_data_pass_()

        is_valid_test = await data_passes_repository.is_data_pass_valid(
            data_pass_id=valid_data_pass.id
        )
        assert is_valid_test

        not_valid_test = await data_passes_repository.is_data_pass_valid(
            data_pass_id=uuid.uuid4()
        )
        assert not not_valid_test

    async def test_is_data_pass_expiry_date(
        self,
        app: FastAPI,
        client: AsyncClient,
        data_passes_repository: DataPassesRepository,
        data_pass_sources_repository: DataPassSourcesRepository,
        valid_data_pass_source_data_for_expiry_test: dict,
        non_expired_data_pass_test_data: dict,
        expired_data_pass_test_data: dict,
        test_data_pass_verifier: TestDataPassVerifier,
    ):
        _data_source = await create_data_source(
            valid_data_pass_source_data_for_expiry_test,
            data_pass_sources_repository,
        )

        _data_verifier = test_data_pass_verifier.data_pass_verifier

        non_expired = await create_data_pass(
            _data_source.id,
            _data_verifier.id,
            non_expired_data_pass_test_data,
            data_passes_repository,
        )
        not_expired_test = await data_passes_repository.is_data_pass_valid(
            data_pass_id=non_expired.id
        )
        assert not_expired_test

        expired = await create_data_pass(
            _data_source.id,
            _data_verifier.id,
            expired_data_pass_test_data,
            data_passes_repository,
        )
        expired_test = await data_passes_repository.is_data_pass_valid(
            data_pass_id=expired.id
        )
        assert not expired_test

    async def test_activate_data_pass(
        self,
        app: FastAPI,
        client: AsyncClient,
        data_passes_repository: DataPassesRepository,
    ):
        valid_data_pass = await data_passes_repository.get_random_data_pass_()

        activation = await data_passes_repository.activate_data_pass(
            data_pass_id=valid_data_pass.id, pda_url="pda_url"
        )
        assert activation is not None
        assert isinstance(activation, IDModelMixin)

    @pytest.mark.xfail(reason="Expected to fail due to db constraints", strict=True)
    async def test_invalid_activate_data_pass(
        self,
        app: FastAPI,
        client: AsyncClient,
        data_passes_repository: DataPassesRepository,
    ):
        await data_passes_repository.activate_data_pass(
            data_pass_id=uuid.uuid4(), pda_url="pda_url"
        )
