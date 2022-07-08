from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SprocketBase(BaseModel):
    teeth: int


class SprocketCreate(SprocketBase):
    ...


class SprocketInDB(SprocketBase):
    uuid: UUID
    created: datetime
    updated: datetime
    widget_uuid: UUID

    class Config:
        orm_mode = True


class Sprocket(SprocketInDB):
    ...
