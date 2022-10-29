import sqlalchemy as sa

from app.core.db import BaseModel, SurrogateKeyMixin, TimestampMixin, SoftDeleteMixin, StrSizes


__all__ = [
    "Role",
    "Grade",
    "Skill",
]


class Role(BaseModel, SurrogateKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "role"

    name: str = sa.Column(sa.String(StrSizes.MD), nullable=False)


class Grade(BaseModel, SurrogateKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "grade"

    name: str = sa.Column(sa.String(StrSizes.MD), nullable=False)


class Skill(BaseModel, SurrogateKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "skill"

    name: str = sa.Column(sa.String(StrSizes.MD), nullable=False)

    max_score: int = sa.Column(sa.Integer, nullable=False)
