"""
This file tests all Merchant routes
All of these routes require a merchant user
TODO: Inject Merchant Dependency
TODO: Parametrize fixture
"""
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


class TestMerchantRoutes:
    @pytest.mark.asyncio
    async def test_merchant_barcode_verify_route_exists(
            self, app: FastAPI
    ) -> None:
        assert app.url_path_for("merchant:barcode:verify") == "/api/merchant/barcode/verify"

    @pytest.mark.xfail(reason="TODO: Merchant Authenticated Route")
    @pytest.mark.asyncio
    async def test_merchant_barcode_verify_route_raises_error_on_invalid(
            self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post(app.url_path_for("merchant:barcode:verify"), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_merchant_scan_transactions_count_route_exists(
            self, app: FastAPI
    ) -> None:
        assert app.url_path_for("merchant:scan_transactions_count") == "/api/merchant/scan_transactions_count"
        assert app.url_path_for("merchant:scan-transactions-count") == "/api/merchant/scan-transactions-count"

    @pytest.mark.xfail(reason="TODO: Merchant Authenticated Route")
    @pytest.mark.asyncio
    async def test_merchant_scan_transactions_count_route_raises_error_on_invalid(
            self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post(app.url_path_for("merchant:scan-transactions-count"), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY
