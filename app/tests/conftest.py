import os
import warnings
from io import BytesIO
from pathlib import Path
from typing import Tuple

import alembic
import pytest
from alembic.config import Config
from asgi_lifespan import LifespanManager
from databases import Database
from fastapi import FastAPI, Response, UploadFile
from fastapi_users.password import get_password_hash
from fastapi_users.user import CreateUserProtocol
from httpx import AsyncClient

from app.apis.utils.random import random_string
from app.core import global_state
from app.db.repositories.activity_log import ActivityLogRepository
# Apply migrations at beginning and end of testing session
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.customers_log import CustomersLogRepository
from app.db.repositories.data_pass_sources import DataPassSourcesRepository
from app.db.repositories.data_pass_verifiers import DataPassVerifiersRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.db.repositories.merchants import MerchantsRepository
from app.db.repositories.scan_transactions import ScanTransactionsRepository
from app.db.repositories.users import UsersRepository
from app.models.merchant import MerchantEmailView, MerchantNew
from app.models.user import UserCreate, UserDB
from app.tests.helpers.data_generator import create_new_merchant

viviane_password_hash = get_password_hash("viviane")


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TEST"] = "1"
    config = Config("/app/alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


# Create a new application for testing
@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.main import app

    return app


@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state.db


# Customers Repo
@pytest.fixture
async def customers_repository(db: Database) -> CustomersRepository:
    return CustomersRepository(db)


# Customers Log Repo
@pytest.fixture
async def customers_log_repository(db: Database) -> CustomersLogRepository:
    return CustomersLogRepository(db)


# Merchants Repo
@pytest.fixture
async def merchants_repository(db: Database) -> MerchantsRepository:
    return MerchantsRepository(db)


# Users Repo
@pytest.fixture
async def users_repository(db: Database) -> UsersRepository:
    return UsersRepository(db)


# Scan Transactions Repo
@pytest.fixture
async def scan_transactions_repository(db: Database) -> ScanTransactionsRepository:
    return ScanTransactionsRepository(db)


# Data Passes Repo
@pytest.fixture
async def data_passes_repository(db: Database) -> DataPassesRepository:
    return DataPassesRepository(db)


# Data Pass Sources Repo
@pytest.fixture
async def data_pass_sources_repository(db: Database) -> DataPassSourcesRepository:
    return DataPassSourcesRepository(db)


# Data Pass Verifiers Repo
@pytest.fixture
async def data_pass_verifiers_repository(db: Database) -> DataPassVerifiersRepository:
    return DataPassVerifiersRepository(db)


@pytest.fixture
async def activity_log_repository(db: Database) -> ActivityLogRepository:
    return ActivityLogRepository(db)


# Make requests in our tests
@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://localhost",
            headers={"Accept": "application/json"},
        ) as client:
            yield client


@pytest.fixture
def customers_test_file() -> UploadFile:
    customer_file = Path("app/tests/data/customers-test.csv")
    with open(customer_file, "rb") as f:
        return UploadFile("customers-test.csv", BytesIO(f.read()), "csv")


# Make sure this number is the number of records in customer_test_file
@pytest.fixture
def customers_test_file_records_number() -> int:
    return 200


@pytest.fixture
def merchants_test_file() -> UploadFile:
    merchant_file = Path("app/tests/data/merchants-test.csv")
    with open(merchant_file, "rb") as f:
        return UploadFile("merchants-test.csv", BytesIO(f.read()), "csv")


# Make sure this number is the number of records in merchant_test_file
@pytest.fixture
def merchants_test_file_records_number() -> int:
    return 1


@pytest.fixture
def test_response():
    return Response()


@pytest.fixture
def superuser() -> UserDB:
    return UserDB(
        email="merlin@camelot.bt",
        hashed_password=viviane_password_hash,
        is_superuser=True,
    )


@pytest.fixture
def merchant_data() -> MerchantNew:
    return create_new_merchant()


@pytest.fixture
async def user_merchant(
    merchants_repository: MerchantsRepository, merchant_data: MerchantNew
) -> Tuple[CreateUserProtocol, MerchantEmailView]:
    # create merchant
    created_merchant = await merchants_repository.create_merchant(
        new_merchant=merchant_data
    )
    await merchants_repository.update_welcome_email_sent(
        merchant_id=created_merchant.id
    )
    user = await global_state.fastapi_users.create_user(
        UserCreate(
            email=merchant_data.email,
            password=random_string(),
            is_verified=True,
        )
    )

    merchant = await merchants_repository.get_merchant_by_email(
        email=merchant_data.email
    )

    return (user, merchant)
