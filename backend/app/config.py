from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Quicklab"
    api_version: str = "0.1.0"
    media_storage_bucket: str = "quicklab-media"
    redis_url: str = "redis://localhost:6379/0"
    whisper_model: str = "tiny"
    database_url: str = "postgresql+asyncpg://quicklab:quicklab@localhost:5432/quicklab"


settings = Settings()
