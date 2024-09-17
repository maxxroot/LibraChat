# app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DOMAIN: str
    SYNC_DATABASE_URL: str
    ASYNC_DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    CORS_ORIGINS: str
    LOG_LEVEL: str

    class Config:
        env_file = ".env"

settings = Settings()
