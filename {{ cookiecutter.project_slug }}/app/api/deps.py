from typing import Generator

from app.db.database import app_database


def get_db() -> Generator:
    try:
        yield app_database.get_database()
    finally:
        pass
