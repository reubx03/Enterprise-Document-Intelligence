from fastapi import APIRouter, File, UploadFile

from app.schemas.upload import UploadResponse
from app.services.upload_service import UploadService

router = APIRouter()

upload_service = UploadService()


@router.post(
    "/upload",
    response_model=UploadResponse,
    summary="Upload a document",
)
async def upload_document(
    file: UploadFile = File(...),
) -> UploadResponse:
    return await upload_service.upload_file(file)