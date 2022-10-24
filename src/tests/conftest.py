from typing import Generator
from urllib.parse import urljoin

import pytest
from httpx import AsyncClient

from app.config import config
from app.core.db import SessionLocal, SessionT


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def client() -> Generator[AsyncClient, None, None]:
    async with AsyncClient(base_url=urljoin("http://127.0.0.1:8000", config.API_PREFIX)) as client:
        yield client


@pytest.fixture(scope="session")
def db() -> Generator[SessionT, None, None]:
    yield SessionLocal()
