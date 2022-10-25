import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.core.db import BaseModel, SurrogateKeyMixin, TimestampMixin, SoftDeleteMixin, StrSizes

__all__ = ["Skill", "Level"]


class Skill(BaseModel, SurrogateKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "career"

    name: str = sa.Column(sa.String(StrSizes.MD), nullable=False)

    level_id: int = sa.Column(sa.ForeignKey("levels.id", ondelete="CASCADE"))
    level: "Level" = relationship("Level", back_populates="career")


class Level(BaseModel, SurrogateKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "levels"

    max_score: int = sa.Column(sa.Integer, nullable=False)

    skills: list["Skill"] = relationship(
        "Skills",
        back_populates="level",
    )
