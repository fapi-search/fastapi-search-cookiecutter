from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .widget import Widget


class InventoryBase(BaseModel):
    widget_uuid: UUID
    widget_count: int


class InventoryUpsert(InventoryBase):
    ...


class InventoryInDB(InventoryBase):
    uuid: UUID
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class Inventory(InventoryInDB):
    ...


class InventoryWithWidgets(Inventory):
    widget: Widget


InventoryWithWidgetsList = list[InventoryWithWidgets]
