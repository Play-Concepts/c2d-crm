"""
This file tests all Merchant routes
All of these routes require a merchant user
TODO: Inject Merchant Dependency
"""
import uuid

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

pytestmark = pytest.mark.asyncio


@pytest.fixture
def test_data_pass_id() -> uuid.UUID:
    return uuid.uuid4()


class TestMerchantRoutes:
    @pytest.mark.parametrize(
        "route_name, route_path, include_data_pass_id",
        [
            ("merchant:barcode_verify", "/api/merchant/{}/barcode/verify", True),
            (
                "merchant:scan_transactions_count",
                "/api/merchant/{}/scan_transactions_count",
                True,
            ),
        ],
    )
    async def test_merchant_routes_exists(
        self,
        app: FastAPI,
        client: AsyncClient,
        route_name: str,
        route_path: str,
        include_data_pass_id: bool,
        test_data_pass_id: uuid.UUID,
    ) -> None:
        if include_data_pass_id:
            assert app.url_path_for(
                route_name, data_pass_id=str(test_data_pass_id)
            ) == route_path.format(str(test_data_pass_id))
        else:
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
