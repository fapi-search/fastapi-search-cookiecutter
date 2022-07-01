from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Path, status

from app.schemas import (
    Inventory,
    InventoryUpsert,
    InventoryWithWidgets,
    InventoryWithWidgetsList,
)

router = APIRouter()


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=Inventory)
async def update_inventory(*, inventory_in: InventoryUpsert) -> Inventory:
    """Update widget_count, create an inventory record if needed"""
    ...


@router.get("/{widget_uuid}", response_model=InventoryWithWidgets)
async def get_inventory_for_widget(
    *, widget_uuid: UUID = Path(title="uuid of widget")
) -> InventoryWithWidgets:
    """Get the inventory for a specific widget"""
    ...


@router.get("/", response_model=InventoryWithWidgetsList)
async def get_widget_inventory_list() -> InventoryWithWidgetsList:
    """Get the inventory for all widgets"""
    ...
