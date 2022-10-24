import typing as t
from pathlib import Path

from pydantic import BaseSettings, DirectoryPath

_BASE_DIR = Path(__file__).parent


class Config(BaseSettings):
    BASE_DIR: DirectoryPath = _BASE_DIR

    API_PREFIX: str = "/api"

    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    SERVER_POSTGRES_CONNECTION: str | None

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
        env_file = _BASE_DIR.parent.parent / ".env"


config = Config()
