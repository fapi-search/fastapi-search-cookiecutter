from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Path, status

from app.schemas import SprocketCreate, Widget, WidgetCreate, WidgetWithSprockets

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Widget)
async def create_widget(*, widget_in: WidgetCreate) -> Widget:
    """Create a widget"""
    ...


@router.get("/{widget_uuid}", response_model=WidgetWithSprockets)
async def get_widget(
    *, widget_uuid: UUID = Path(title="uuid of widget")
) -> WidgetWithSprockets:
    """Get a widget"""
    ...


@router.put("/{widget_uuid}", response_model=WidgetWithSprockets)
async def add_sprocket(
    *, widget_uuid: UUID = Path(title="uuid of widget"), sprocket_in: SprocketCreate
) -> WidgetWithSprockets:
    """Add a sprocket to a widget"""
    ...
