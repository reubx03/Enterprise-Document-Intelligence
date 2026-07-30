from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ----------------------------
    # Application Configuration
    # ----------------------------
    app_name: str
    environment: str

    # ----------------------------
    # External Services
    # ----------------------------
    database_url: str
    qdrant_url: str
    n8n_url: str

    # ----------------------------
    # Upload Configuration
    # ----------------------------
    upload_directory: str
    max_upload_size: int
    allowed_file_types: str

    # ----------------------------
    # OCR Configuration
    # ----------------------------
    tesseract_cmd: str
    poppler_path: str
    ocr_language: str
    pdf_dpi: int
    ocr_output_directory: str
    ocr_confidence_threshold: float

    # ----------------------------
    # LLM Extraction
    # ----------------------------
    gemini_api_key: str
    gemini_model: str
    extraction_max_tokens: int
    extraction_temperature: float
    extraction_confidence_threshold: float

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()