"""
This file tests the api path /api/auth/create-password.
It shares the same path as fastapi_users:auth
This is a custom endpoint, which must be tested
"""
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

pytestmark = pytest.mark.asyncio


class TestCustomAuthCreatePasswordRoutes:
    async def test_create_password_route_exist(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post(app.url_path_for("auth:create-password"), json={})
        assert res.status_code != HTTP_404_NOT_FOUND
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    # TODO Test the Actual Create Password API
