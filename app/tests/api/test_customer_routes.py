"""
This file tests all Customer routes
All of these routes require a pda_user
TODO: Inject PDA Dependency
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


class TestCustomerRoutes:
    @pytest.mark.parametrize(
        "route_name, route_path",
        [
            ("customer:check-first-login", "/api/customer/check-first-login"),
        ],
    )
    async def test_customer_routes_exists(
        self, app: FastAPI, client: AsyncClient, route_name: str, route_path: str
    ) -> None:
        assert app.url_path_for(route_name) == route_path

    @pytest.mark.parametrize(
        "route_name, route_path",
        [
            ("customer:search", "/api/customer/data/{}/search"),
            ("customer:claim", "/api/customer/data/{}/claim"),
        ],
    )
    async def test_customer_routes_with_data_pass_id_exists(
        self,
        app: FastAPI,
        client: AsyncClient,
        route_name: str,
        route_path: str,
        test_data_pass_id: uuid.UUID,
    ) -> None:
        assert app.url_path_for(
            route_name, data_pass_id=str(test_data_pass_id)
        ) == route_path.format(str(test_data_pass_id))

    @pytest.mark.parametrize(
        "route_name",
        [
            "customer:search",
            "customer:claim",
            "customer:check-first-login",
        ],
    )
    @pytest.mark.xfail(reason="TODO: PDA Authenticated Route")
    async def test_customer_routes_raise_error_on_invalid(
        self,
        app: FastAPI,
        client: AsyncClient,
        route_name: str,
    ) -> None:
        res = await client.post(app.url_path_for(route_name), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY
