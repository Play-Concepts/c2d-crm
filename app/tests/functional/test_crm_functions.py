import pytest
from fastapi import FastAPI
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestCrmFunctions:
    @pytest.mark.xfail(
        reason="IGNORING: no additional codes in function to test. "
        "Tested by ../db/test_customers_repository::get_customers"
    )
    async def test_fn_list_customers(
        self,
        app: FastAPI,
        client: AsyncClient,
    ) -> None:
        assert False

    @pytest.mark.xfail(reason="TODO")
    async def test_fn_get_customer(
        self,
        app: FastAPI,
        client: AsyncClient,
    ) -> None:
        assert True

    @pytest.mark.xfail(reason="TODO")
    async def test_fn_customer_upload(
        self,
        app: FastAPI,
        client: AsyncClient,
    ) -> None:
        assert True

    @pytest.mark.xfail(reason="TODO")
    async def test_fn_merchant_upload(
        self,
        app: FastAPI,
        client: AsyncClient,
    ) -> None:
        assert True
