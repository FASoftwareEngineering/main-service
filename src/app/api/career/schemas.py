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


class SkillsBase(BaseSchema):
    name: str
    max_score: int


class SkillsCreate(SkillsBase):
    pass


class SkillsUpdate(SkillsBase):
    name: str | None = None
    max_score: int | None = None


class SkillsRead(SkillsBase):
    id: int
