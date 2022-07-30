from __future__ import annotations

import json
from uuid import UUID

from databases import Database
from fastapi import APIRouter, BackgroundTasks, Body, Depends, Path, status

from app.api import deps
from app.db.search import AsyncSearch
from app.schemas import SprocketCreate, Widget, WidgetCreate, WidgetWithSprockets

router = APIRouter()


async def update_search(widget: Widget, search_db: AsyncSearch) -> None:
    response = await search_db.index(
        index="widgets", {% if cookiecutter.search_backend == "elasticsearch" %}document{% elif cookiecutter.search_backend == "opensearch" %}body{% endif %}=widget.dict(), id=widget.uuid, refresh=True
    )
    if response["result"] not in ["created", "updated"]:
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

    sql = """
    INSERT
        INTO
        widget (name)
    VALUES (
        :name
    ) RETURNING *
    """
    from_db = await app_db.fetch_one(sql, widget_in.dict())
    widget = Widget.from_orm(from_db)
    background_tasks.add_task(update_search, widget, search_db)
    return widget


@router.get("/{uuid}", response_model=WidgetWithSprockets)
async def get_widget(
    *,
    uuid: UUID = Path(description="widget uuid"),
    app_db: Database = Depends(deps.get_app_db),
) -> WidgetWithSprockets:
    """Get a widget"""

    fetch_sql = """
    SELECT
        widget.*,
        (
            SELECT
                array_to_json(array_agg(row_to_json(sprockets)))
            FROM
                (
                    SELECT
                        sprocket.*
                    FROM
                        sprocket
                    WHERE
                        sprocket.widget_uuid = widget.uuid
                ) sprockets
        ) sprockets
    FROM
        widget
    WHERE
        widget.uuid = :widget_uuid
    """
    from_db = await app_db.fetch_one(fetch_sql, values={"widget_uuid": uuid})
    from_db.sprockets = json.loads(from_db.sprockets)
    widget = WidgetWithSprockets.from_orm(from_db)
    return widget


@router.put("/{uuid}", response_model=WidgetWithSprockets)
async def add_sprockets(
    *,
    uuid: UUID = Path(description="widget uuid"),
    sprockets: list[SprocketCreate] = Body(
        title="Sprockets to create and add to widget"
    ),
    background_tasks: BackgroundTasks,
    app_db: Database = Depends(deps.get_app_db),
    search_db: AsyncSearch = Depends(deps.get_search_db),
) -> WidgetWithSprockets:
    """Add a sprockets to a widget"""

    async with app_db.transaction():
        insert_sql = """
        INSERT
            INTO
            sprocket (
                teeth,
                widget_uuid
            )
        VALUES (
            :teeth,
            :widget_uuid
        )
        """
        await app_db.execute_many(
            query=insert_sql,
            values=[dict(widget_uuid=uuid, **s.dict()) for s in sprockets],
        )

        fetch_sql = """
        SELECT
            widget.*,
            (
                SELECT
                    array_to_json(array_agg(row_to_json(sprockets)))
                FROM
                    (
                        SELECT
                            sprocket.*
                        FROM
                            sprocket
                        WHERE
                            sprocket.widget_uuid = widget.uuid
                    ) sprockets
            ) sprockets
        FROM
            widget
        WHERE
            widget.uuid = :widget_uuid
        """
        from_db = await app_db.fetch_one(fetch_sql, values={"widget_uuid": uuid})
        from_db.sprockets = json.loads(from_db.sprockets)
    widget = WidgetWithSprockets.from_orm(from_db)
    background_tasks.add_task(update_search, widget, search_db)
    return widget
