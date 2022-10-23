import typing as t

from pydantic.generics import GenericModel

from app.core.schemas import BaseSchema

_T = t.TypeVar("_T", bound=BaseSchema)


class PaginationSchema(GenericModel, t.Generic[_T]):
    offset: int | None
    limit: int | None
    total: int
    results: list[_T]
