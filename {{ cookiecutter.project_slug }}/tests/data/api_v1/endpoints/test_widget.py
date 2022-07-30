from __future__ import annotations

import pytest
from async_asgi_testclient import TestClient
from databases import Database
from fastapi import FastAPI, status

from app.schemas import Sprocket, Widget


@pytest.mark.asyncio
async def test_create_widget(
    async_client: TestClient, app: FastAPI, app_db: Database
) -> None:
    # run sut
    url = app.url_path_for("create_widget")
    response = await async_client.post(url, json={"name": "mega widget"})

    # validate response
    assert response.status_code == status.HTTP_201_CREATED

    # validate data
    from_db = await app_db.fetch_one(
        "SELECT * FROM widget WHERE uuid = :uuid", {"uuid": response.json()["uuid"]}
    )
    assert Widget.from_orm(from_db) == Widget(**response.json())


@pytest.mark.asyncio
async def test_add_sprockets(
    widget: Widget, async_client: TestClient, app: FastAPI, app_db: Database
) -> None:
    # run sut
    url = app.url_path_for("add_sprockets", uuid=widget.uuid)
    sprocket_teeth = [{"teeth": teeth} for teeth in range(5)]
    response = await async_client.put(url, json=sprocket_teeth)

    # validate response
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["uuid"] == str(widget.uuid)

    # validate data
    from_db = await app_db.fetch_one(
        "SELECT * FROM widget WHERE uuid = :uuid", {"uuid": response.json()["uuid"]}
    )
    assert Widget.from_orm(from_db) == Widget(**response.json())

    from_db = await app_db.fetch_all(
        "SELECT * FROM sprocket WHERE widget_uuid = :widget_uuid",
        {"widget_uuid": widget.uuid},
    )
    assert [Sprocket.from_orm(db) for db in from_db] == [
        Sprocket(**api) for api in response.json()["sprockets"]
    ]


@pytest.mark.asyncio
async def test_get_widget_with_sprockets(
    widget_with_sprockets: Widget,
    async_client: TestClient,
    app: FastAPI,
    app_db: Database,
) -> None:
    # run sut
    url = app.url_path_for("get_widget", uuid=widget_with_sprockets.uuid)
    response = await async_client.get(url)

    # validate response
    assert response.status_code == status.HTTP_200_OK

    # validate data
    from_db = await app_db.fetch_one(
        "SELECT * FROM widget WHERE uuid = :uuid", {"uuid": response.json()["uuid"]}
    )
    assert Widget.from_orm(from_db) == Widget(**response.json())

    from_db = await app_db.fetch_all(
        "SELECT * FROM sprocket WHERE widget_uuid = :widget_uuid",
        {"widget_uuid": widget_with_sprockets.uuid},
    )
    assert [Sprocket.from_orm(db) for db in from_db] == [
        Sprocket(**api) for api in response.json()["sprockets"]
    ]
