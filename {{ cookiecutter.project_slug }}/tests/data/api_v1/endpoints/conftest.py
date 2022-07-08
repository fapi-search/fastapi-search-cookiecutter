from __future__ import annotations

import pytest_asyncio
from async_asgi_testclient import TestClient
from databases import Database
from fastapi import FastAPI

from app.schemas import Widget


@pytest_asyncio.fixture
async def widget(async_client: TestClient, app: FastAPI, app_db: Database) -> Widget:
    url = app.url_path_for("create_widget")
    post_response = await async_client.post(url, json={"name": "widget"})
    return Widget(**post_response.json())
