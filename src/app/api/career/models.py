import sqlalchemy as sa


from app.core.db import BaseModel, SurrogateKeyMixin, TimestampMixin, SoftDeleteMixin, StrSizes

__all__ = [
    "Role",
    "Grade",

]


class Role(BaseModel, SurrogateKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "role"

    name: str = sa.Column(sa.String(StrSizes.MD), nullable=False)

class Grade(BaseModel, SurrogateKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "grade"

    name: str = sa.Column(sa.String(StrSizes.MD), nullable=False)