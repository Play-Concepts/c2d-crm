"""
This file tests the api path /api/auth/*

Authentication Routes are mostly provided for by FastAPIUsers. There is no need to write tests for them, since they
have included tests. We only need to check that they are installed at the correct routes

The exception is /api/auth/create-password. This is a custom endpoint, which must be tested
"""
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY


class TestAuthRoutes:
    @pytest.mark.asyncio
    async def test_login_route_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post("/api/auth/jwt/login", json={})
        assert res.status_code != HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_login_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post("/api/auth/jwt/login", json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_forgot_password_route_exist(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post("/api/auth/forgot-password", json={})
        assert res.status_code != HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_forgot_password_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post("/api/auth/forgot-password", json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_reset_password_route_exist(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post("/api/auth/reset-password", json={})
        assert res.status_code != HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_reset_password_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post("/api/auth/reset-password", json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY


class TestAuthCreatePasswordRoutes:
    @pytest.mark.asyncio
    async def test_create_password_route_exist(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post("/api/auth/create-password", json={})
        assert res.status_code != HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_create_password_input_raises_error(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post("/api/auth/create-password", json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    # TODO Test the Actual Create Password API
