import sqlalchemy as sa

from app.api.users.constants import UserTypes
from app.core.db import BaseModel, SoftDeleteMixin, StrSizes, SurrogateKeyMixin, TimestampMixin

__all__ = [
    "User",
]


# Single Table Inheritance - несколько типов классов представлены одной таблицей:
# https://docs.sqlalchemy.org/en/14/orm/inheritance.html#single-table-inheritance
class User(BaseModel, SurrogateKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "user"

    type: UserTypes = sa.Column(sa.Enum(UserTypes))

    sso_id: str = sa.Column(sa.String(StrSizes.SSO), index=True)
    email: str = sa.Column(sa.String(StrSizes.SM), unique=True, nullable=False)
    phone: str = sa.Column(sa.String(StrSizes.SM), unique=True, nullable=False)

    first_name: str = sa.Column(sa.String(StrSizes.SM), nullable=False)
    last_name: str = sa.Column(sa.String(StrSizes.SM), nullable=False)
    middle_name: str = sa.Column(sa.String(StrSizes.SM))

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": UserTypes.user,
    }
