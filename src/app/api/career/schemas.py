from app.core.schemas import BaseSchema


class RoleBase(BaseSchema):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    name: str | None = None


class RoleRead(RoleBase):
    id: int


class GradeBase(BaseSchema):
    name: str


class GradeCreate(GradeBase):
    pass


class GradeUpdate(GradeBase):
    name: str | None = None


class GradeRead(GradeBase):
    id: int


class SkillBase(BaseSchema):
    name: str
    max_score: int


class SkillCreate(SkillBase):
    pass


class SkillUpdate(SkillBase):
    name: str | None = None
    max_score: int | None = None


class SkillRead(SkillBase):
    id: int
