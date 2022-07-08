from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from fastapi import APIRouter, Body, Path, status

from app.schemas import (
    Sprocket,
    SprocketCreate,
    Widget,
    WidgetCreate,
    WidgetWithSprockets,
)

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Widget)
async def create_widget(*, widget_in: WidgetCreate) -> Widget:
    """Create a widget (MOCKED)"""

    now = datetime.now()
    return Widget(created=now, updated=now, uuid=uuid4(), **widget_in.dict())


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
