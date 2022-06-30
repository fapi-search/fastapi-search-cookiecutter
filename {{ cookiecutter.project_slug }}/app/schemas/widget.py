from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .sprocket import Sprocket


class WidgetBase(BaseModel):
    name: str


class WidgetCreate(WidgetBase):
    ...


class WidgetInDB(WidgetBase):
    uuid: UUID
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class Widget(WidgetInDB):
    ...


class WidgetWithSprockets(Widget):
    sprockets: list[Sprocket]
