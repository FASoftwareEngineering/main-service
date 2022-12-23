import typing as t
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import sql

from app.core.db import SessionT, SoftDeleteMixin, SurrogateKeyMixin

_M = t.TypeVar("_M", bound=t.Union[SurrogateKeyMixin, SoftDeleteMixin])


class CRUD(t.Generic[_M]):
    """Generic CRUD methods

    Generic-реализация репозитория для выполнения CRUD операций над объектами,
    производными от SurrogateKeyMixin и SoftDeleteMixin
    """

    def __init__(self, session: SessionT, model_cls: t.Type[_M]):
        self.session = session
        self.model_cls = model_cls

    def save(self, entity: _M, commit: bool = True) -> _M:
        self.session.add(entity)
        if commit:
            self.session.commit()
        else:
            self.session.flush()
        return entity

    def save_all(self, entities: list[_M], commit: bool = True) -> list[_M]:
        self.session.add_all(entities)
        if commit:
            self.session.commit()
        else:
            self.session.flush()
        return entities

    def get_by_id(self, id_: int, _include_deleted: bool = False) -> _M | None:
        exec_opts = {"_include_deleted": _include_deleted}
        return self.session.get(self.model_cls, id_, execution_options=exec_opts)

    def get_all(self, _include_deleted: bool = False) -> list[_M]:
        exec_opts = {"_include_deleted": _include_deleted}
        stmt = sql.select(self.model_cls)
        return self.session.scalars(stmt, execution_options=exec_opts).all()

    def get_all_paginate(
        self,
        offset: int = None,
        limit: int = None,
        _include_deleted: bool = False,
    ) -> tuple[list[_M], int]:
        exec_opts = {"_include_deleted": _include_deleted}
        stmt = sql.select(self.model_cls).offset(offset).limit(limit)
        total = self.session.scalar(sql.select(sql.func.count()).select_from(self.model_cls))
        return self.session.scalars(stmt, execution_options=exec_opts).all(), total

    def delete(self, entity: _M, soft: bool = True) -> None:
        if soft:
            soft_delete(self.session, entity, commit=False)
        else:
            self.session.delete(entity)

    def delete_by_id(self, id_: int, soft: bool = True) -> bool:
        if soft:
            entity = self.get_by_id(id_)
            if entity is None:
                return False
            soft_delete(self.session, entity, commit=False)
            return True

        stmt = sql.delete(self.model_cls).where(self.model_cls.id == id_)
        res = self.session.execute(stmt)
        return res.rowcount > 0  # type: ignore


def count_rows(session: SessionT, stmt) -> int:
    return session.scalar(sql.select(sql.func.count()).select_from(stmt))


def soft_delete(session: SessionT, entity: _M, commit: bool = True) -> None:
    entity.deleted = True

    for col in entity.__table__.columns:
        # TODO: что если имя колонки отличается от имени атрибута?
        # TODO: обработать множественный UniqueConstraint
        # TODO: для VARCHAR обработать максимальную длину
        # TODO: что делать с другими типами данных?
        if (col.primary_key or col.unique) and isinstance(col.type, sa.String):
            attr = getattr(entity, col.name)
            timestamp_prefix = int(datetime.utcnow().timestamp())
            setattr(entity, col.name, f"{timestamp_prefix}::{attr}")

    session.add(entity)
    if commit:
        session.commit()
