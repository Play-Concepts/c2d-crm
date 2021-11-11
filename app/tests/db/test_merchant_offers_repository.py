from typing import List, Tuple

import pytest
from fastapi import FastAPI
from fastapi_users.user import CreateUserProtocol
from httpx import AsyncClient

from app.db.repositories.merchant_offers import MerchantOffersRepository
from app.models.merchant import MerchantEmailView
from app.models.merchant_offer import MerchantOfferNew
from app.tests.helpers.data_generator import create_new_merchant_offer

pytestmark = pytest.mark.asyncio

NUMBER_OF_TEST_RECORDS = 5


class TestMerchantOffersRepository:
    async def test_get_customer_offers(
        self,
        app: FastAPI,
        client: AsyncClient,
        merchant_offers_repository: MerchantOffersRepository,
        user_merchant: Tuple[CreateUserProtocol, MerchantEmailView],
    ):
        def new_merchant_offers_test_data(
            u_merchant: Tuple[CreateUserProtocol, MerchantEmailView]
        ) -> List[MerchantOfferNew]:
            _, merchant = u_merchant
            return [
                create_new_merchant_offer(merchant.id)
                for _ in range(NUMBER_OF_TEST_RECORDS)
            ]

        merchant_offers_test_data = new_merchant_offers_test_data(user_merchant)
        for merchant_offer_data in merchant_offers_test_data:
            await merchant_offers_repository.create_merchant_offer(
                merchant_offer_new=merchant_offer_data
            )

        assert True

    async def test_like_merchant_offer(
        self,
        app: FastAPI,
        client: AsyncClient,
        merchant_offers_repository: MerchantOffersRepository,
    ):
        assert True

    async def test_unlike_merchant_offer(
        self,
        app: FastAPI,
        client: AsyncClient,
        merchant_offers_repository: MerchantOffersRepository,
    ):
        assert True

    async def test_get_customer_favourited_offers(
        self,
        app: FastAPI,
        client: AsyncClient,
        merchant_offers_repository: MerchantOffersRepository,
    ):
        assert True

    async def test_get_all_customer_offers(
        self,
        app: FastAPI,
        client: AsyncClient,
        merchant_offers_repository: MerchantOffersRepository,
    ):
        assert True
