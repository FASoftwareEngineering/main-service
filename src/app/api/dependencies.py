import typing as t

from app.core.db import SessionT, db
from app.core.schemas import BaseSchema


def get_session() -> t.Generator[SessionT, None, None]:
    session = db.session_factory()
    try:
        yield session
    finally:
        session.close()


class PaginationQuery(BaseSchema):
    offset: int | None = None
    limit: int | None = None
