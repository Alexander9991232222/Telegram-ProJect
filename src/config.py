import os
from pathlib import Path

from pydantic import SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    bot_token: SecretStr
    db_path: str = os.path.join(BASE_DIR, "db", "database.db")

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


try:
    settings = Settings()
except ValidationError as e:
    print(f"Failed to load settings: {e}")
    raise
