from __future__ import annotations

import random

from async_asgi_testclient import TestClient
from fastapi import FastAPI, status

from app.schemas import Widget


async def test_create_widget(async_client: TestClient, app: FastAPI) -> None:
    url = app.url_path_for("create_widget")
    response = await async_client.post(url, json={"name": "mega widget"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "mega widget"


async def test_get_widget(
    async_client: TestClient, app: FastAPI, widget: Widget
) -> None:
    url = app.url_path_for("get_widget", uuid=widget.uuid)
    response = await async_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["uuid"] == str(widget.uuid)


async def test_add_sprockets(
    async_client: TestClient, app: FastAPI, widget: Widget
) -> None:
    url = app.url_path_for("add_sprockets", uuid=widget.uuid)
    sprocket_teeth = [{"teeth": random.randrange(1, 10)} for _ in range(10)]
    response = await async_client.put(url, json=sprocket_teeth)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["uuid"] == str(widget.uuid)
    assert sprocket_teeth == [
        {"teeth": sprocket["teeth"]} for sprocket in response.json()["sprockets"]
    ]
