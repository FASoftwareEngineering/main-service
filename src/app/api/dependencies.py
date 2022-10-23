import typing as t

from fastapi import Query

from app.core.db import SessionT, SessionLocal
from app.core.schemas import BaseSchema


def get_session() -> t.Generator[SessionT, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


class PaginationQuery(BaseSchema):
    offset: int | None = None
    limit: int | None = None


def pagination_query(offset: int | None = Query(None), limit: int | None = Query(None)) -> PaginationQuery:
    return PaginationQuery(offset=offset, limit=limit)
