from fastapi import APIRouter, status, Depends

from app import models
from app.api.constants import Prefixes, Tags
from app.api.career import schemas
from typing import List

from app.api.services import CRUD

roles_router = APIRouter(prefix=f"/{Prefixes.roles}", tags=[Tags.roles])
grades_router = APIRouter(prefix=f"/{Prefixes.grades}", tags=[Tags.grades])
skills_router = APIRouter(prefix=f"/{Prefixes.skills}", tags=[Tags.skills])


@roles_router.get("/{role_id}", response_model=schemas.RolesRead)
def get_role(
        role_id: int,
        # session: SessionT = Depends(get_session),
        crud: CRUD[models.Roles] = Depends(get_crud),
):
    pass


# поправить
@roles_router.get("", response_model=List[schemas.RolesRead])
def get_roles():
    # session: SessionT = Depends(get_session),
    # crud: CRUD[models.Roles] = Depends(get_crud),
    pass


@roles_router.post("", response_model=schemas.RolesRead, status_code=status.HTTP_201_CREATED)
def create_role(
        data: schemas.RolesCreate,
        # session: SessionT = Depends(get_session),
        # crud: CRUD[models.Roles] = Depends(get_crud),
):
    pass


@roles_router.patch("/{role_id}", response_model=schemas.RolesRead)
def update_role(
        data: schemas.RolesUpdate,
        # session: SessionT = Depends(get_session),
        # crud: CRUD[models.Roles] = Depends(get_crud),
):
    pass


@roles_router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
        role_id: int,
        # session: SessionT = Depends(get_session),
        # crud: CRUD[models.Roles] = Depends(get_crud),
):
    pass


# grades
@grades_router.get("/{grade_id}", response_model=schemas.GradesRead)
def get_grade(
        grade_id: int,
        # session: SessionT = Depends(get_session),
        # crud: CRUD[models.Grades] = Depends(get_crud),



router.get("/{skill_id}", response_model=schemas.SkillsRead)
def get_skill(
    skill_id: int,
):
    pass


@grades_router.get("", response_model=List[schemas.GradesRead])
def get_grades():
    # session: SessionT = Depends(get_session),
    # crud: CRUD[models.Grades] = Depends(get_crud),
    pass


@grades_router.post("", response_model=schemas.GradesRead, status_code=status.HTTP_201_CREATED)
def create_grade(
        data: schemas.GradesReadradesCreate,
        # session: SessionT = Depends(get_session),
        # crud: CRUD[models.Grades] = Depends(get_crud),
        
        
@grades_router.patch("/{grade_id}", response_model=schemas.GradesRead)
def update_grade(
      data: schemas.GradesUpdate,
      # session: SessionT = Depends(get_session),
      # crud: CRUD[models.Grades] = Depends(get_crud),
):
  pass
        
        
@grades_router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(
        grade_id: int,
        # session: SessionT = Depends(get_session),
        # crud: CRUD[models.Grades] = Depends(get_crud),


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
