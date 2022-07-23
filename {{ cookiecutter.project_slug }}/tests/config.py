from __future__ import annotations

import pathlib

from databases import DatabaseURL
from pydantic import BaseSettings

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent
ENV_FILE = ROOT.parent / ".env"


class TestSettings(BaseSettings):

    TEST_APP_DATABASE_URL: str | DatabaseURL = DatabaseURL(
        "{{ cookiecutter.default_postgres_url | test_database_url }}"  # noqa: E501
    )

    TEST_SEARCH_DATABASE_URL: str | DatabaseURL = DatabaseURL(
        "{{ cookiecutter.default_search_url }}"  # noqa: E501
    )

    class Config:
        case_sensitive = True
        env_file = ENV_FILE
        env_file_encoding = "utf-8"


test_settings = TestSettings()
