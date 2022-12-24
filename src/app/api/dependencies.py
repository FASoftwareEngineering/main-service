import typing as t

from app.core.db import SessionT, db
from app.core.schemas import BaseSchema


def get_session() -> t.Generator[SessionT, None, None]:
    with db.session_factory() as session:
        yield session


class PaginationQuery(BaseSchema):
    offset: int | None = None
    limit: int | None = None
