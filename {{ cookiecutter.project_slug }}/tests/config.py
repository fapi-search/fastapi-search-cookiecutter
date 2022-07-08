from __future__ import annotations

import pathlib

from databases import DatabaseURL
from pydantic import BaseSettings

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class TestSettings(BaseSettings):

    TEST_APP_DATABASE_URL: str | DatabaseURL = DatabaseURL(
        "postgresql+asyncpg://db_user:db_pass@localhost:5432/test_app_db"
    )

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


test_settings = TestSettings()
