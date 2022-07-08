from __future__ import annotations

import pytest
from fastapi import FastAPI

from app.core.config import Settings
from app.core.config import settings as app_settings
from app.main import app as main_app


@pytest.fixture
def settings() -> Settings:
    return app_settings


@pytest.fixture
def app() -> FastAPI:
    return main_app
