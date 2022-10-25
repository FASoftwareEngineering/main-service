import sqlalchemy as sa


from app.core.db import BaseModel, SurrogateKeyMixin, TimestampMixin, SoftDeleteMixin, StrSizes

__all__ = ["Skill"]


class Skill(BaseModel, SurrogateKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "skill"

    name: str = sa.Column(sa.String(StrSizes.MD), nullable=False)

    max_score: int = sa.Column(sa.Integer, nullable=False)
