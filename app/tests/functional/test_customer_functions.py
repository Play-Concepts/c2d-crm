import pytest
from fastapi import FastAPI
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestCustomerFunctions:
    @pytest.mark.xfail(reason="TODO")
    async def test_fn_get_customer_basic(
        self,
        app: FastAPI,
        client: AsyncClient,
    ) -> None:
        assert True

    @pytest.mark.xfail(reason="TODO")
    async def test_fn_search_customers(
        self,
        app: FastAPI,
        client: AsyncClient,
    ) -> None:
        assert True

    @pytest.mark.xfail(reason="TODO")
    async def test_fn_claim_data(
        self,
        app: FastAPI,
        client: AsyncClient,
    ) -> None:
        assert True

    @pytest.mark.xfail(reason="TODO")
    async def test_fn_check_first_login(
        self,
        app: FastAPI,
        client: AsyncClient,
    ) -> None:
        assert True
