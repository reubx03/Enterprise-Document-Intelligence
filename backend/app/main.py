from fastapi import FastAPI

from app.api.v1.router import router as api_router
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)

app.include_router(api_router, prefix="/api/v1")