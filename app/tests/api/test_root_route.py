import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_404_NOT_FOUND

pytestmark = pytest.mark.asyncio


class TestRootRoute:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.get(app.url_path_for("root:hello"))
        assert res.status_code != HTTP_404_NOT_FOUND
