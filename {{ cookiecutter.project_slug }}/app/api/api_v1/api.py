from __future__ import annotations

from fastapi import APIRouter

from app.api.api_v1.endpoints import inventory, widget

api_router = APIRouter()
api_router.include_router(widget.router, prefix="/widgets", tags=["widgets"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
