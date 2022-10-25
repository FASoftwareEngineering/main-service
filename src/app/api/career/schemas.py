from app.core.schemas import BaseSchema


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
