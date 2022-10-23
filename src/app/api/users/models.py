import sqlalchemy as sa

from app.api.users.constants import UserTypes
from app.core.db import BaseModel, SurrogateKeyMixin, TimestampMixin, SoftDeleteMixin

__all__ = [
    "User",
]


# Single Table Inheritance - несколько типов классов представлены одной таблицей:
# https://docs.sqlalchemy.org/en/14/orm/inheritance.html#single-table-inheritance
class User(BaseModel, SurrogateKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "user"

    sso_id: str = sa.Column(sa.String(36))
    type: UserTypes = sa.Column(sa.Enum(UserTypes))

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": UserTypes.user,
    }
