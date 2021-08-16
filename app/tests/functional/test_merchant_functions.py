import pytest
from fastapi import FastAPI
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestCustomerFunctions:
    @pytest.mark.xfail(reason="TODO")
    async def fn_verify_barcode(
        self,
        app: FastAPI,
        client: AsyncClient,
    ) -> None:
        assert True

    @pytest.mark.xfail(reason="TODO")
    async def fn_get_scan_transactions_count(
        self,
        app: FastAPI,
        client: AsyncClient,
    ) -> None:
        assert True
