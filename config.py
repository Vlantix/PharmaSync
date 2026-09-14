from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field
import os

ENV = os.getenv("APP_ENV", "dev")

class Settings(BaseSettings):
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_USER: str = "postgres"
    DATABASE_NAME: str
    DATABASE_PASSWORD: str
    APP_NAME: str = "PharmaSync"
    SECRET_KEY: str
    DEBUG: bool = True
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @computed_field
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    model_config = SettingsConfigDict(
        env_file = f".env.{ENV}",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
