from __future__ import annotations

import pytest
from async_asgi_testclient import TestClient
from fastapi import FastAPI


@pytest.fixture
async def async_client(app: FastAPI) -> TestClient:
    async with TestClient(app) as client:
        yield client
