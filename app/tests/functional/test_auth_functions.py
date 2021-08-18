import pytest
from fastapi import FastAPI
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestAuthFunctions:
    @pytest.mark.xfail(reason="IGNORING: no additional codes in function to test.")
    async def test_fn_created_password(
        self,
        app: FastAPI,
        client: AsyncClient,
    ) -> None:
        assert False
