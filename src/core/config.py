from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
import re


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(..., env="PROJECT_NAME")
    ENV: str = Field("production", env="ENV")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")  # Para Alembic (sync)
    API_PORT: int = Field(8000, env="API_PORT")
    SYNC_DATABASE_URL: str = Field(..., env="SYNC_DATABASE_URL")  # Para Alembic (sync)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        # Para SQLAlchemy async
        return re.sub(r"^postgresql:", "postgresql+asyncpg:", self.DATABASE_URL)


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
