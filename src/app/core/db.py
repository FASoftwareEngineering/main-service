from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import (
    ORMExecuteState,
    Session,
    as_declarative,
    declarative_mixin,
    sessionmaker,
    with_loader_criteria,
)

from app.config import config

__all__ = [
    "engine",
    "SessionLocal",
    "SessionT",
    "BaseModel",
    "SurrogateKeyMixin",
    "TimestampMixin",
    "SoftDeleteMixin",
    "StrSizes",
]

engine = sa.create_engine(
    config.SQLALCHEMY_DATABASE_URI,
    echo=config.SQLALCHEMY_ECHO,
    future=True,
)

SessionLocal = sessionmaker(engine, future=True)
SessionT = Session


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


@sa.event.listens_for(Session, "do_orm_execute")
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
    XS = 16
    SM = 32
    MD = 64
    LG = 128
    XL = 256
    SSO = 36
