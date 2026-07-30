from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.upload import router as upload_router
from app.api.v1.ocr import router as ocr_router

router = APIRouter()

router.include_router(health_router)
router.include_router(upload_router)
router.include_router(ocr_router)