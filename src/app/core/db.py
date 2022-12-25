from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import (
    ORMExecuteState,
    Session,
    as_declarative,
    declarative_mixin,
    sessionmaker,
    with_loader_criteria,
)

from app.config import Config

__all__ = [
    "Database",
    "db",
    "SessionT",
    "BaseModel",
    "SurrogateKeyMixin",
    "TimestampMixin",
    "SoftDeleteMixin",
    "StrSizes",
    "OnDelete",
]

SessionT = Session


class Database:
    _config: Config
    _engine: Engine
    _session_factory: sessionmaker

    def __init__(self, config: Config = None):
        if config:
            self.configure(config)

    def configure(self, config: Config) -> None:
        self._config = config
        self._engine = sa.create_engine(config.SQLALCHEMY_DATABASE_URI, echo=config.DEBUG, future=True)
        self._session_factory = sessionmaker(self._engine, future=True)

    @property
    def engine(self) -> Engine:
        return self._engine

    @property
    def session_factory(self) -> sessionmaker:
        return self._session_factory


db = Database()


@as_declarative()
class BaseModel:
    pass


@declarative_mixin
class SurrogateKeyMixin:
    id: int = sa.Column("id", sa.Integer, primary_key=True, autoincrement=True)


@declarative_mixin
class TimestampMixin:
    created_at: datetime = sa.Column(
        sa.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at: datetime = sa.Column(
        sa.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


@declarative_mixin
class SoftDeleteMixin:
    deleted: bool = sa.Column(sa.Boolean, default=False, nullable=False)


@event.listens_for(Session, "do_orm_execute")
def _add_filtering_criteria(execute_state: ORMExecuteState):
    if (
        not execute_state.is_column_load
        and not execute_state.is_relationship_load
        and not execute_state.execution_options.get("_include_deleted", False)
    ):
        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(
                SoftDeleteMixin,
                lambda x: x.deleted == sa.false(),
                include_aliases=True,
            ),
        )


class StrSizes:
    # дополнительное пространство для реализации soft-delete
    XS = 16 + 16
    SM = 32 + 16
    MD = 64 + 16
    LG = 128 + 16
    XL = 256 + 16


class OnDelete:
    RESTRICT = "RESTRICT"
    CASCADE = "CASCADE"
    SET_NULL = "SET NULL"
