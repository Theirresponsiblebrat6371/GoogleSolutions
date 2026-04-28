from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:password@localhost:5432/smart_resource"
    google_maps_api_key: str = ""
    firebase_api_key: str = ""
    firebase_project_id: str = ""
    secret_key: str = "smart_resource_secret_2026"
    app_port: int = 8000
    match_radius_km: float = 10.0
    priority_threshold: int = 70
    default_city: str = "Bhilai"
    debug: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
