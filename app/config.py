from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., description="Database URL")
    SECRET_KEY: str = Field(..., description="Secret key")
    ALGORITHM: str = Field(..., description="Algorithm")
    EXPIRE_ACCESS_FROM_MINUTES: str = Field(
        ..., description="Expiration time in minutes"
    )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
