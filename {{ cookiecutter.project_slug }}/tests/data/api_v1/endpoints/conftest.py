from __future__ import annotations

import pytest_asyncio
from async_asgi_testclient import TestClient
from databases import Database
from fastapi import FastAPI

from app.schemas import Widget


@pytest_asyncio.fixture
async def widget(async_client: TestClient, app: FastAPI, app_db: Database) -> Widget:
    url = app.url_path_for("create_widget")
    response = await async_client.post(url, json={"name": "test widget"})
    return Widget(**response.json())


@pytest_asyncio.fixture
async def widget_with_sprockets(
    widget: Widget, async_client: TestClient, app: FastAPI, app_db: Database
) -> Widget:
    url = app.url_path_for("add_sprockets", uuid=widget.uuid)
    response = await async_client.put(
        url, json=[{"teeth": teeth} for teeth in range(10)]
    )
    return Widget(**response.json())
