import typing as t
from pathlib import Path
from urllib.parse import urljoin

import pytest
from dotenv import load_dotenv
from factory import random
from fastapi import FastAPI
from httpx import AsyncClient

if t.TYPE_CHECKING:
    from app.config import Config
    from app.core.db import SessionT

load_dotenv(Path(__file__).parent.parent.parent / ".env.test")


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment() -> None:
    random.reseed_random(0)


@pytest.fixture(scope="session")
def app() -> FastAPI:
    from app.main import app

    return app


@pytest.fixture(scope="session")
def config() -> "Config":
    from app.config import config

    return config


@pytest.fixture(scope="session")
def session() -> t.Generator["SessionT", None, None]:
    from app.core.db import SessionLocal

    return SessionLocal()


@pytest.fixture
def runtime_db() -> t.Generator[None, None, None]:
    from app.core.db import BaseModel, engine

    BaseModel.metadata.create_all(engine)
    yield
    BaseModel.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="module")
async def client(app, config) -> t.Generator[AsyncClient, None, None]:
    async with AsyncClient(
        app=app,
        base_url=urljoin("http://127.0.0.1:8000", config.API_PREFIX),
    ) as client:
        yield client
