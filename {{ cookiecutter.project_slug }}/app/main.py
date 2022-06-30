from pathlib import Path

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.templating import Jinja2Templates

from app.api.api_v1.api import api_router
from app.core.config import settings

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

root_router = APIRouter()
app = FastAPI(title="{{ cookiecutter.project_name }}")


@root_router.get("/", status_code=200)
def root(
    request: Request,
) -> Response:
    """
    Root GET
    """
    return TEMPLATES.TemplateResponse("index.html", {"request": request})


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn  # type: ignore

    uvicorn.run(app, host="{{ cookiecutter.default_host }}", port={{ cookiecutter.default_port }}, log_level="debug")
