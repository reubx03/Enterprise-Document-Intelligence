from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    environment: str

    database_url: str
    qdrant_url: str
    n8n_url: str

    # Upload Configuration
    upload_directory: str
    max_upload_size: int
    allowed_file_types: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()