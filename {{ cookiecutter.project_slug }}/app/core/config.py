from __future__ import annotations

import pathlib

from databases import DatabaseURL
from pydantic import AnyHttpUrl, BaseSettings, validator

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200"]'  # noqa: E800
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    APP_DATABASE_URL: str | DatabaseURL = DatabaseURL(
        "{{ cookiecutter.default_postgres_url }}"  # noqa: E501
    )

    SEARCH_DATABASE_URL: str | DatabaseURL = DatabaseURL(
        "{{ cookiecutter.default_search_url }}"  # noqa: E501
    )

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
