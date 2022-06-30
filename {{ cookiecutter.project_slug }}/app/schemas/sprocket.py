from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SprocketBase(BaseModel):
    teeth: int
    widget_uuid: UUID


class SprocketCreate(SprocketBase):
    ...


class SprocketInDB(SprocketBase):
    uuid: UUID
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class Sprocket(SprocketInDB):
    ...
