from typing import Generator

import pytest

from app.core.db import SessionLocal, SessionT


@pytest.fixture(scope="session")
def session() -> Generator[SessionT, None, None]:
    yield SessionLocal()
