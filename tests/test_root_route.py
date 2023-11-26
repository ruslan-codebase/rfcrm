from pytest import mark, fixture
from httpx import AsyncClient
from typing import AsyncGenerator
from app.main import app


@fixture(scope="function")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://testfastapi.localhost") as client:
        yield client


@mark.asyncio
async def test_root_route(async_client):
    async for cl in async_client:
        resp = await cl.get("/")
        assert resp is not None
        assert resp.status_code == 200
        assert resp.json() == {"message": "Welcome to RFCRM"}
        await cl.aclose()

