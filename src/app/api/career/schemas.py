from app.core.schemas import BaseSchema


class RolesBase(BaseSchema):
    name: str


class RolesCreate(RolesBase):
    pass


class RolesUpdate(RolesBase):
    name: str | None = None


class RolesRead(RolesBase):
    id: int


class GradesBase(BaseSchema):
    name: str


class GradesCreate(GradesBase):
    pass


class GradesUpdate(GradesBase):
    name: str | None = None


class GradesRead(GradesBase):
    id: int


class GradesSchema(GradesBase):
    authors: list[RolesBase]


class RolesSchema(RolesBase):
    books: list[GradesBase]
