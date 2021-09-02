import uuid
from datetime import datetime, timedelta
from typing import List

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.db.repositories.data_passes import DataPassesRepository
from app.models.core import IDModelMixin
from app.tests.helpers.data_creator import (create_data_pass,
                                            create_data_source_and_verifier)
from app.tests.helpers.data_generator import (
    create_new_data_pass_data, create_valid_data_pass_source_verifier_data)

pytestmark = pytest.mark.asyncio


NUMBER_OF_TEST_RECORDS = 5


@pytest.fixture(scope="class")
def valid_data_pass_source_verifier_data() -> dict:
    return create_valid_data_pass_source_verifier_data()


@pytest.fixture(scope="class")
def valid_data_pass_test_data() -> List[dict]:
    return [
        create_new_data_pass_data("active", None) for _ in range(NUMBER_OF_TEST_RECORDS)
    ]


@pytest.fixture(scope="class")
def valid_data_pass_source_verifier_data_for_expiry_test() -> dict:
    return create_valid_data_pass_source_verifier_data()


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
        valid_data_pass_source_verifier_data: dict,
        valid_data_pass_test_data: dict,
    ):
        _data_source_and_verifier = await create_data_source_and_verifier(
            valid_data_pass_source_verifier_data, data_passes_repository
        )
        for valid_data_pass_data in valid_data_pass_test_data:
            await create_data_pass(
                _data_source_and_verifier.id,
                valid_data_pass_data,
                data_passes_repository,
            )

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
        valid_data_pass_source_verifier_data_for_expiry_test: dict,
        non_expired_data_pass_test_data: dict,
        expired_data_pass_test_data: dict,
    ):
        _data_source_and_verifier = await create_data_source_and_verifier(
            valid_data_pass_source_verifier_data_for_expiry_test, data_passes_repository
        )

        non_expired = await create_data_pass(
            _data_source_and_verifier.id,
            non_expired_data_pass_test_data,
            data_passes_repository,
        )
        not_expired_test = await data_passes_repository.is_data_pass_valid(
            data_pass_id=non_expired.id
        )
        assert not_expired_test

        expired = await create_data_pass(
            _data_source_and_verifier.id,
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
