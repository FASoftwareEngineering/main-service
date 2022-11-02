import os
from typing import Generator
from urllib.parse import urljoin

import pytest
from factory import random
from httpx import AsyncClient

os.environ["APP_DEBUG"] = "False"
os.environ["APP_DB_URI"] = "postgresql://postgres:123456@127.0.0.1:5432/test-main-service-bd"

from app.main import app  # noqa
from app.config import config  # noqa
from app.core.db import BaseModel, engine  # noqa


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    random.reseed_random(0)


@pytest.fixture
def db() -> Generator[None, None, None]:
    BaseModel.metadata.create_all(engine)
    yield
    BaseModel.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="module")
async def client() -> Generator[AsyncClient, None, None]:
    async with AsyncClient(
        app=app,
        base_url=urljoin("http://127.0.0.1:8000", config.API_PREFIX),
    ) as client:
        yield client
