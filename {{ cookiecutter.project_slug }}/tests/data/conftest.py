from __future__ import annotations

import pytest_asyncio
from async_asgi_testclient import TestClient
from databases import Database, DatabaseURL
from fastapi import FastAPI

from app.db.database import app_database
from app.db.search import search_database

from ..config import test_settings

test_app_db_url = DatabaseURL(test_settings.TEST_APP_DATABASE_URL)
assert test_app_db_url.database.startswith(
    "test"
), "test database name must start with 'test'"
app_database.config(test_app_db_url, force_rollback=True)

test_search_db_url = DatabaseURL(test_settings.TEST_SEARCH_DATABASE_URL)
search_database.config(test_search_db_url)


@pytest_asyncio.fixture
async def async_client(app: FastAPI) -> TestClient:
    async with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def app_db() -> Database:
    await app_database.connect()
    await search_database.connect()
    yield await app_database.get_database()
    await app_database.disconnect()
    await search_database.disconnect()
