from __future__ import annotations
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database (MySQL)
    database_url: str = "mysql+pymysql://app_user:app_password@127.0.0.1:3306/timbre_share?charset=utf8mb4"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_hours: int = 24

    # MinIO / Local storage fallback
    storage_backend: str = "local"
    data_dir: str = str(Path(__file__).resolve().parent.parent / "data")

    # Server
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    cors_origins: str = "http://localhost:5173,http://localhost:5500,http://127.0.0.1:5500"

    # SMS (stub for MVP)
    sms_enabled: bool = False

    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
