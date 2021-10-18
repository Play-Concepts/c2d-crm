import pytest
from faker import Faker
from faker.providers import misc
from fastapi import FastAPI
from httpx import AsyncClient

from app.apis.utils.random import random_string
from app.core import global_state
from app.db.repositories.merchants import MerchantsRepository
from app.db.repositories.users import UsersRepository
from app.models.merchant import MerchantEmailView, MerchantNew
from app.models.user import UserCreate, UserView
from app.tests.helpers.data_generator import create_new_merchant

fake = Faker()
fake.add_provider(misc)

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="class")
def new_merchant() -> MerchantNew:
    return create_new_merchant()


# setup
@pytest.fixture
async def active_merchant(
    merchants_repository: MerchantsRepository, new_merchant: MerchantNew
) -> MerchantEmailView:
    # create merchant
    created_merchant = await merchants_repository.create_merchant(
        new_merchant=new_merchant,
    )
    await merchants_repository.update_welcome_email_sent(
        merchant_id=created_merchant.id
    )
    await global_state.fastapi_users.create_user(
        UserCreate(
            email=new_merchant.email,
            password=random_string(),
            is_verified=False,
        )
    )

    return await merchants_repository.get_merchant_by_email(email=new_merchant.email)


class TestUsersRepository:
    async def test_create_password(
        self,
        app: FastAPI,
        client: AsyncClient,
        users_repository: UsersRepository,
        active_merchant: MerchantEmailView,
    ) -> None:
        repo_to_test: UsersRepository = users_repository
        result = await repo_to_test.create_password(
            token=active_merchant.password_change_token,
            password=fake.password(length=12),
        )
        assert result is not None
        assert isinstance(result, UserView)
        assert result.email == active_merchant.email
