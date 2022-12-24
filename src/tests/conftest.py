import typing as t
from urllib.parse import urljoin

import pytest
import sqlalchemy as sa
from factory import random
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.engine import make_url, Engine
from sqlalchemy.orm import close_all_sessions

from app.config import Config
from app.core.db import SessionT, db, BaseModel
from app.main import create_app


@pytest.fixture(scope="session", autouse=True)
def setup_factory_boy() -> None:
    random.reseed_random(0)


@pytest.fixture(scope="session")
def config() -> Config:
    conf = Config()
    conf.DEBUG = False
    url = make_url(conf.SQLALCHEMY_DATABASE_URI).set(database="app_tests_postgres")
    conf.SQLALCHEMY_DATABASE_URI = str(url)
    conf.SENTRY_DSN = None
    return conf


@pytest.fixture(scope="session")
def app(config: Config) -> FastAPI:
    return create_app(config)


@pytest.fixture(scope="session")
def test_db(config: Config) -> t.Generator:
    url = make_url(config.SQLALCHEMY_DATABASE_URI)
    engine = sa.create_engine(url.set(database="postgres"), isolation_level="AUTOCOMMIT", future=True)

    with engine.begin() as conn:
        exists = conn.scalar(sa.text(f"SELECT true FROM pg_database WHERE datname = '{url.database}'"))
        if not exists:
            conn.execute(sa.text(f"CREATE DATABASE {url.database}"))

    yield

    with engine.begin() as conn:
        text = f"""
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE datname = '{url.database}' AND pid <> pg_backend_pid()
        """
        conn.execute(sa.text(text))
        conn.execute(sa.text(f"DROP DATABASE IF EXISTS {url.database}"))


@pytest.fixture(scope="session")
def engine(app: FastAPI) -> Engine:
    return db.engine


@pytest.fixture(scope="session")
def session(app: FastAPI) -> SessionT:
    return db.session_factory()


def _create_all_tables(engine: Engine) -> None:
    close_all_sessions()
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)


def _drop_all_tables(engine: Engine) -> None:
    close_all_sessions()
    BaseModel.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def runtime_tables_module(test_db, engine: Engine) -> t.Generator:
    _create_all_tables(engine)
    yield
    _drop_all_tables(engine)


@pytest.fixture(scope="function")
def runtime_tables_function(test_db, engine: Engine) -> t.Generator:
    _create_all_tables(engine)
    yield
    _drop_all_tables(engine)


@pytest.fixture(scope="module")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="module")
async def client(app: FastAPI, config: Config) -> t.Generator[AsyncClient, None, None]:
    async with AsyncClient(
        app=app,
        base_url=urljoin("http://127.0.0.1:8000", config.API_PREFIX),
    ) as client:
        yield client
