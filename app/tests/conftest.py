import os
import warnings

import alembic
import pytest
import requests
import requests as requests
from alembic.config import Config
from asgi_lifespan import LifespanManager
from databases import Database
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi_users.password import get_password_hash
from httpx import AsyncClient

# Apply migrations at beginning and end of testing session
from app.models.user import UserDB

viviane_password_hash = get_password_hash("viviane")


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
    from app.main import app as application

    return application


# Grab a reference to our database when needed
@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state.db


# Make requests in our tests
@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client


@pytest.fixture
def superuser() -> UserDB:
    return UserDB(
        email="merlin@camelot.bt",
        hashed_password=viviane_password_hash,
        is_superuser=True,
    )


@pytest.fixture
def merchant() -> UserDB:
    return UserDB(
        email="morgana@camelot.bt",
        hashed_password=viviane_password_hash,
        is_superuser=False,
    )


@pytest.fixture(scope="session")
def pda_user():
    r = requests.get(
        "https://testing.hubat.net/users/access_token",
        headers={"username": "testing", "password": "labai-geras-slaptazodis"},
    )
    return r.json()["accessToken"]
