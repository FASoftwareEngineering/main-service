import typing as t
from pathlib import Path

from pydantic import BaseSettings, DirectoryPath, Field

_BASE_DIR = Path(__file__).parent
_ENV_PREFIX = "APP_"


class Config(BaseSettings):
    BASE_DIR: DirectoryPath = _BASE_DIR
    DEBUG: bool = Field(default=False, env=f"{_ENV_PREFIX}DEBUG")

    API_PREFIX: str = "/api"

    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    SQLALCHEMY_DATABASE_URI: str | None = Field(env=f"{_ENV_PREFIX}DB_URI")
    SQLALCHEMY_ECHO: bool = DEBUG

    LOGGING_CONFIG: dict[str, t.Any] = {
        "handlers": [
            {
                "sink": "sys.stderr",
                "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:^8} | {name}:{line} - {message}",
                "level": "DEBUG",
            },
        ],
    }

    class Config:
        """ENV config"""

        env_file = _BASE_DIR.parent.parent / ".env"
        env_prefix = _ENV_PREFIX


config = Config()
