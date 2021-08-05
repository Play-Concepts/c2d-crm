"""
This file tests the api path /api/auth/*

Authentication Routes are mostly provided for by FastAPIUsers. There is no need to write tests for them, since they
have included tests. We only need to check that they are installed at the correct routes

The exception is /api/auth/create-password. This is a custom endpoint, which must be tested
"""
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


class TestCrmCustomersRoutes:
    @pytest.mark.asyncio
    async def test_list_customers_route_exist(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.get(app.url_path_for("crm:list_customers"))
        assert res.status_code != HTTP_404_NOT_FOUND

    @pytest.mark.xfail(reason="TODO: Authenticated Route")
    @pytest.mark.asyncio
    async def test_get_customer_route_exist(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.get(
            app.url_path_for("crm:get_customer", path_params="/dummy")
        )
        assert res.status_code == HTTP_201_CREATED

    @pytest.mark.xfail(reason="TODO: Authenticated Route")
    @pytest.mark.asyncio
    async def test_upload_customers_route_exists_and_raises_error_on_invalid(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post(app.url_path_for("crm:upload_customers"), json={})
        assert res.status_code != HTTP_404_NOT_FOUND
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY


class TestCrmMerchantsRoutes:
    @pytest.mark.xfail(reason="TODO: Authenticated Route")
    @pytest.mark.asyncio
    async def test_upload_merchants_route_exists_and_raises_error_on_invalid(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post(app.url_path_for("crm:upload_merchants"), json={})
        assert res.status_code != HTTP_404_NOT_FOUND
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY
