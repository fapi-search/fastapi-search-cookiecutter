from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.templating import Jinja2Templates

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.database import app_database
from app.db.search import search_database

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

root_router = APIRouter()
app = FastAPI(title="{{ cookiecutter.project_name }}")


@app.on_event("startup")
async def startup_event() -> None:
    app_database.config(settings.APP_DATABASE_URL)
    await app_database.connect()
    search_database.config(settings.SEARCH_DATABASE_URL)
    await search_database.connect()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await app_database.disconnect()
    await search_database.disconnect()


@root_router.get("/", status_code=200)
def root(request: Request) -> Response:
    """Root GET"""
    return TEMPLATES.TemplateResponse("index.html", {"request": request})


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="{{ cookiecutter.default_local_host }}", port="{{ cookiecutter.default_local_port }}", log_level="debug")
