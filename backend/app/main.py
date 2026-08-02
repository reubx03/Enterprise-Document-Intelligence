from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.router import router as api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.exceptions.pipeline_exceptions import (
    PipelineExtractionStageError,
    PipelineOCRStageError,
)
from app.exceptions.upload_exceptions import (
    FileStorageError,
    FileTooLargeError,
    InvalidFileTypeError,
)

# Configure logging
setup_logging()

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)

# Register API routes
app.include_router(api_router, prefix="/api/v1")


# -----------------------------
# Exception Handlers
# -----------------------------

@app.exception_handler(InvalidFileTypeError)
async def invalid_file_type_handler(
    request: Request,
    exc: InvalidFileTypeError,
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc),
        },
    )


@app.exception_handler(FileTooLargeError)
async def file_too_large_handler(
    request: Request,
    exc: FileTooLargeError,
):
    return JSONResponse(
        status_code=413,
        content={
            "detail": str(exc),
        },
    )


@app.exception_handler(FileStorageError)
async def file_storage_handler(
    request: Request,
    exc: FileStorageError,
):
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
        },
    )


@app.exception_handler(PipelineOCRStageError)
async def pipeline_ocr_handler(
    request: Request,
    exc: PipelineOCRStageError,
):
    return JSONResponse(
        status_code=500,
        content={
            "stage": "ocr",
            "detail": str(exc),
        },
    )


@app.exception_handler(PipelineExtractionStageError)
async def pipeline_extraction_handler(
    request: Request,
    exc: PipelineExtractionStageError,
):
    return JSONResponse(
        status_code=500,
        content={
            "stage": "extraction",
            "detail": str(exc),
        },
    )