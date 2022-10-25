from app.core.schemas import BaseSchema


class SkillsBase(BaseSchema):
    name: str
    level_id: int


class SkillsCreate(SkillsBase):
    pass


class SkillsUpdate(SkillsBase):
    name: str | None = None
    level_id: int | None = None


class SkillsRead(SkillsBase):
    id: int


class LevelsBase(BaseSchema):
    max_score: int


class LevelsCreate(LevelsBase):
    pass


class LevelsUpdate(LevelsBase):
    max_score: int | None = None


class LevelsRead(LevelsBase):
    id: int
