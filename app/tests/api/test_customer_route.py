"""
This file tests all Customer routes
All of these routes require a pda_user
TODO: Inject PDA Dependency
TODO: Parametrize fixture
"""
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY


class TestCustomerRoutes:
    @pytest.mark.asyncio
    async def test_customer_basic_route_exists(self, app: FastAPI) -> None:
        assert app.url_path_for("customer:basic") == "/api/customer/basic"

    @pytest.mark.asyncio
    async def test_customer_search_route_exists(self, app: FastAPI) -> None:
        assert app.url_path_for("customer:search") == "/api/customer/search"

    @pytest.mark.xfail(reason="TODO: PDA Authenticated Route")
    @pytest.mark.asyncio
    async def test_customer_search_route_raises_error_on_invalid(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post(app.url_path_for("customer:search"), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_customer_claim_route_exists(self, app: FastAPI) -> None:
        assert app.url_path_for("customer:claim") == "/api/customer/claim"

    @pytest.mark.xfail(reason="TODO: PDA Authenticated Route")
    @pytest.mark.asyncio
    async def test_customer_claim_route_raises_error_on_invalid(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post(app.url_path_for("customer:claim"), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_customer_check_first_login_route_exists(self, app: FastAPI) -> None:
        assert (
            app.url_path_for("customer:check-first-login")
            == "/api/customer/check-first-login"
        )

    @pytest.mark.xfail(reason="TODO: PDA Authenticated Route")
    @pytest.mark.asyncio
    async def test_customer_check_first_login_route_raises_error_on_invalid(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post(app.url_path_for("customer:check-first-login"), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY
