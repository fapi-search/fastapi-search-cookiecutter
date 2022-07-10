from __future__ import annotations

from typing import AsyncGenerator

from databases import Database

from app.db.database import app_database
from app.db.search import AsyncSearch, search_database


async def get_app_db() -> AsyncGenerator[Database, None]:
    try:
        yield await app_database.get_database()
    finally:
        pass


async def get_search_db() -> AsyncGenerator[AsyncSearch, None]:
    try:
        yield await search_database.get_database()
    finally:
        pass
