from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from databases import Database
from fastapi import APIRouter, BackgroundTasks, Body, Depends, Path, status

from app.api import deps
from app.db.search import AsyncSearch
from app.schemas import (
    Sprocket,
    SprocketCreate,
    Widget,
    WidgetCreate,
    WidgetWithSprockets,
)

router = APIRouter()


async def update_search(widget: Widget, search_db: AsyncSearch) -> None:
    response = await search_db.index(
        index="widgets", {% if cookiecutter.search_backend == "elasticsearch" %}document{% elif cookiecutter.search_backend == "opensearch" %}body{% endif %}=widget.dict(), id=widget.uuid, refresh=True
    )
    if response["result"] not in ["created"]:
        print(response)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Widget)
async def create_widget(
    *,
    widget_in: WidgetCreate,
    background_tasks: BackgroundTasks,
    app_db: Database = Depends(deps.get_app_db),
    search_db: AsyncSearch = Depends(deps.get_search_db),
) -> Widget:
    """Create a widget"""

    sql = """INSERT INTO widget (name) VALUES (:name) RETURNING *"""
    from_db = await app_db.fetch_one(sql, widget_in.dict())
    widget = Widget.from_orm(from_db)
    background_tasks.add_task(update_search, widget, search_db)
    return widget


@router.get("/{uuid}", response_model=WidgetWithSprockets)
async def get_widget(
    *, uuid: UUID = Path(description="widget uuid")
) -> WidgetWithSprockets:
    """Get a widget (MOCKED)"""

    now = datetime.now()
    return WidgetWithSprockets(
        created=now, updated=now, uuid=uuid, sprockets=[], name=str(uuid)
    )


@router.put("/{uuid}", response_model=WidgetWithSprockets)
async def add_sprockets(
    *,
    uuid: UUID = Path(description="widget uuid"),
    sprockets: list[SprocketCreate] = Body(
        title="Sprockets to create and add to widget"
    ),
) -> WidgetWithSprockets:
    """Add a sprockets to a widget (MOCKED)"""

    now = datetime.now()
    return WidgetWithSprockets(
        created=now,
        updated=now,
        uuid=uuid,
        sprockets=[
            Sprocket(
                uuid=uuid4(),
                widget_uuid=uuid,
                teeth=sprocket.teeth,
                created=now,
                updated=now,
            )
            for sprocket in sprockets
        ],
        name=str(uuid),
    )
