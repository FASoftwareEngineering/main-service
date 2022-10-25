from fastapi import APIRouter, status

from app.api.constants import Prefixes, Tags
from app.api.career import schemas

skills_router = APIRouter(prefix=f"/{Prefixes.skills}", tags=[Tags.skills])


@skills_router.get("/{skill_id}", response_model=schemas.SkillsRead)
def get_skill(
    skill_id: int,
):
    pass


@skills_router.get("", response_model=list[schemas.SkillsRead])
def get_skills():
    pass


@skills_router.post("", response_model=schemas.SkillsRead, status_code=status.HTTP_201_CREATED)
def create_skill(
    data: schemas.SkillsCreate,
):
    pass


@skills_router.patch("/{skill_id}", response_model=schemas.SkillsRead)
def update_skill(
    data: schemas.SkillsUpdate,
):
    pass


@skills_router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(
    skill_id: int,
):
    pass
