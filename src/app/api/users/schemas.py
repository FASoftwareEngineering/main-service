from app.api.schemas import PaginationSchema
from app.api.users.constants import PublicUserTypes
from app.core.schemas import BaseSchema


class UserBase(BaseSchema):
    type: PublicUserTypes

    sso_id: str
    email: str
    phone: str

    first_name: str
    last_name: str
    middle_name: str | None = None


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    type: PublicUserTypes | None = None
    sso_id: str | None = None
    email: str | None = None
    phone: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserRead(UserBase):
    id: int


class UserPagination(PaginationSchema[UserRead]):
    pass


class UserFilterQuery(BaseSchema):
    type: PublicUserTypes | None = None
    sso_id: str | None = None
    email: str | None = None
    phone: str | None = None
    first_name: str | None = None
    last_name: str | None = None
