from fastapi import APIRouter, status

from app.api.career import schemas
from app.api.constants import Prefixes, Tags

roles_router = APIRouter(prefix=f"/{Prefixes.roles}", tags=[Tags.roles])
grades_router = APIRouter(prefix=f"/{Prefixes.grades}", tags=[Tags.grades])
skills_router = APIRouter(prefix=f"/{Prefixes.skills}", tags=[Tags.skills])


# -------------- Roles


@roles_router.get("/{role_id}", response_model=schemas.RoleRead)
def get_role(
    role_id: int,
):
    pass


@roles_router.get("", response_model=list[schemas.RoleRead])
def get_roles():
    pass


@roles_router.post("", response_model=schemas.RoleRead, status_code=status.HTTP_201_CREATED)
def create_role(
    data: schemas.RoleCreate,
):
    pass


@roles_router.patch("/{role_id}", response_model=schemas.RoleRead)
def update_role(
    data: schemas.RoleUpdate,
):
    pass


@roles_router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: int,
):
    pass


# -------------- Grades


@grades_router.get("/{grade_id}", response_model=schemas.GradeRead)
def get_grade(
    grade_id: int,
):
    pass


@grades_router.get("", response_model=list[schemas.GradeRead])
def get_grades():
    pass


@grades_router.post("", response_model=schemas.GradeRead, status_code=status.HTTP_201_CREATED)
def create_grade(
    data: schemas.GradeCreate,
):
    pass


@grades_router.patch("/{grade_id}", response_model=schemas.GradeRead)
def update_grade(
    data: schemas.GradeUpdate,
):
    pass


@grades_router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(
    grade_id: int,
):
    pass


# -------------- Skills


@skills_router.get("/{skill_id}", response_model=schemas.SkillRead)
def get_skill(
    skill_id: int,
):
    pass


@skills_router.get("", response_model=list[schemas.SkillRead])
def get_skills():
    pass


@skills_router.post("", response_model=schemas.SkillRead, status_code=status.HTTP_201_CREATED)
def create_skill(
    data: schemas.SkillCreate,
):
    pass


@skills_router.patch("/{skill_id}", response_model=schemas.SkillRead)
def update_skill(
    data: schemas.SkillUpdate,
):
    pass


@skills_router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(
    skill_id: int,
):
    pass
