import sys
from pathlib import Path
from typing import Any

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from loguru import logger

# The root of the project is added to the Python path. This allows the script to import
# modules from the root directory.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.api import api_router  # noqa: E402
from app.config import settings, setup_app_logging  # noqa: E402

# setup logging as early as possible
setup_app_logging(config=settings)

# Create an instance of FastAPI. The title of the application and the URL for the OpenAPI schema
# are set using the application's settings.
app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Create an instance of APIRouter. This will be used to define the API endpoints.
root_router = APIRouter()

# Define a GET endpoint at /. When accessed, it returns a basic HTML response.
@root_router.get("/")
def index(request: Request) -> Any:
    """Basic HTML response."""
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Welcome to the API</h1>"
        "<div>"
        "Check the docs: <a href='/docs'>here</a>"
        "</div>"
        "</body>"
        "</html>"
    )

    return HTMLResponse(content=body)

# The API router and the root router are included in the FastAPI application.
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

# If the BACKEND_CORS_ORIGINS setting is set, the CORSMiddleware is added to the FastAPI application.
# This allows the application to accept cross-origin requests from the specified origins.
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8001, log_level="debug")
