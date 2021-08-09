import asyncio
from typing import List

import pytest
from faker import Faker
from faker.providers import company, internet, misc
from fastapi import FastAPI
from httpx import AsyncClient

from app.apis.utils.random import random_string
from app.core import global_state
from app.db.repositories.merchants import MerchantsRepository
from app.db.repositories.users import UsersRepository
from app.models.merchant import MerchantEmailView, MerchantNew
from app.models.user import UserCreate, UserView

fake = Faker()
fake.add_provider(company)
fake.add_provider(internet)
fake.add_provider(misc)

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="class")
def new_merchant() -> MerchantNew:
    company_name = fake.company()
    return MerchantNew(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        company_name="{} {}".format(company_name, fake.company_suffix()),
        trade_name=company_name,
        address=fake.address(),
        email=fake.company_email(),
        phone_number=fake.phone_number(),
        offer={
            "description": fake.catch_phrase(),
            "start_date": fake.date(),
            "end_date": fake.date(),
        },
        logo_url=fake.image_url(),
        terms_agreed=fake.boolean(chance_of_getting_true=50),
    )


# setup
@pytest.fixture
async def active_merchant(
    merchants_repository: MerchantsRepository, new_merchant: MerchantNew
) -> MerchantEmailView:
    # create merchant\
    await merchants_repository.create_merchant(new_merchant=new_merchant)
    await global_state.fastapi_users.create_user(
        UserCreate(
            email=new_merchant.email,
            password=random_string(),
            is_verified=False,
        )
    )

    merchants: List[
        MerchantEmailView
    ] = await merchants_repository.get_merchants_email_list()
    return merchants[0]


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
