"""
This file tests the api path /api/auth/*

Authentication Routes are mostly provided for by FastAPIUsers. There is no need to write tests for them, since they
have included tests. We only need to check that they are installed at the correct routes

The exception is /api/auth/create-password. This is a custom endpoint, which must be tested
"""
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

pytestmark = pytest.mark.asyncio


class TestCrmRoutes:
    @pytest.mark.parametrize(
        "route_name, route_path",
        [
            ("crm:list_customers", "/api/crm/customers"),
            ("crm:upload_customers", "/api/crm/customers/upload"),
            ("crm:upload_merchants", "/api/crm/merchants/upload"),
        ],
    )
    async def test_crm_routes_exists(
        self, app: FastAPI, client: AsyncClient, route_name: str, route_path: str
    ) -> None:
        assert app.url_path_for(route_name) == route_path

    @pytest.mark.parametrize(
        "route_name",
        [
            "crm:upload_merchants",
            "crm:upload_customers",
        ],
    )
    @pytest.mark.xfail(reason="TODO: CRM Authenticated Route")
    async def test_merchant_routes_raise_error_on_invalid(
        self,
        app: FastAPI,
        client: AsyncClient,
        route_name: str,
    ) -> None:
        res = await client.post(app.url_path_for(route_name), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY
