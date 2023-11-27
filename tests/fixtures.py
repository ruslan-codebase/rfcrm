from pytest import fixture
from httpx import AsyncClient
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.in_mem_sqlite_database import InMemSqliteDatabase
from app.db import db
from app.main import app


test_db = InMemSqliteDatabase()

@fixture(scope="function")
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    await test_db.init_db()
    async for test_session in test_db.get_session():
        yield test_session
    await test_db.destroy_db()


@fixture(scope="function")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    await test_db.init_db()
    app.dependency_overrides[db.get_session] = test_db.get_session
    async with AsyncClient(app=app, base_url="http://testfastapi.localhost") as client:
        yield client
    await test_db.destroy_db()
