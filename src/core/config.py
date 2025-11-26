from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
import re


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(..., env="PROJECT_NAME")
    ENV: str = Field("production", env="ENV")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DB_DRIVER: str = Field("psycopg", env="DB_DRIVER")
    API_PORT: int = Field(8000, env="API_PORT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        url = re.sub(
            r"^postgresql://", f"postgresql+{self.DB_DRIVER}://", self.DATABASE_URL
        )
        return url


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
