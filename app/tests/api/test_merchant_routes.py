"""
This file tests all Merchant routes
All of these routes require a merchant user
TODO: Inject Merchant Dependency
"""
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

pytestmark = pytest.mark.asyncio


class TestMerchantRoutes:
    @pytest.mark.parametrize(
        "route_name, route_path",
        [
            ("merchant:barcode:verify", "/api/merchant/barcode/verify"),
            (
                "merchant:scan_transactions_count",
                "/api/merchant/scan_transactions_count",
            ),
            (
                "merchant:scan-transactions-count",
                "/api/merchant/scan-transactions-count",
            ),
        ],
    )
    async def test_merchant_routes_exists(
        self, app: FastAPI, client: AsyncClient, route_name: str, route_path: str
    ) -> None:
        assert app.url_path_for(route_name) == route_path

    @pytest.mark.parametrize(
        "route_name",
        [
            "merchant:barcode:verify",
        ],
    )
    @pytest.mark.xfail(reason="TODO: Merchant Authenticated Route")
    async def test_merchant_routes_raise_error_on_invalid(
        self,
        app: FastAPI,
        client: AsyncClient,
        route_name: str,
    ) -> None:
        res = await client.post(app.url_path_for(route_name), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    # TODO To implement scan-transactions-count logic check
