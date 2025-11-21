from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(..., env="PROJECT_NAME")
    POSTGRES_HOST: str = Field(..., env="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(..., env="POSTGRES_PORT")
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
