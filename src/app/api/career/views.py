from fastapi import APIRouter, status, Depends

from app.api.career import schemas, models, services
from app.api.constants import Prefixes, Tags
from app.api.dependencies import get_session
from app.api.exceptions import raise_404
from app.api.services import CRUD
from app.core.db import SessionT

roles_router = APIRouter(prefix=f"/{Prefixes.roles}", tags=[Tags.roles])
grades_router = APIRouter(prefix=f"/{Prefixes.grades}", tags=[Tags.grades])
skills_router = APIRouter(prefix=f"/{Prefixes.skills}", tags=[Tags.skills])


def get_roles_crud(session: SessionT = Depends(get_session)) -> CRUD[models.Role]:
    return services.roles_crud_factory(session)


def valid_role_id(role_id: int, crud: CRUD[models.Role] = Depends(get_roles_crud)) -> models.Role:
    role = crud.get_by_id(role_id)
    if not role:
        raise_404(message=f"Role with id={role_id} not found")
    return role


@roles_router.get("/{role_id}", response_model=schemas.RoleRead)
def get_role(
    role: models.Role = Depends(valid_role_id),
):
    return role


@roles_router.get("", response_model=list[schemas.RoleRead])
def get_roles(
    crud: CRUD[models.Role] = Depends(get_roles_crud),
):
    return crud.get_all()


@roles_router.post("", response_model=schemas.RoleRead, status_code=status.HTTP_201_CREATED)
def create_role(
    data: schemas.RoleCreate,
    session: SessionT = Depends(get_session),
):
    new_data = data.dict()
    grade_ids = [grade.id for grade in data.grades]
    new_data["grades"] = services.get_grades_by_ids(session, grade_ids)

    role = models.Role(**new_data)

    session.add(role)
    session.commit()
    return role


@roles_router.patch("/{role_id}", response_model=schemas.RoleRead)
def update_role(
    data: schemas.RoleUpdate,
    role: models.Role = Depends(valid_role_id),
    session: SessionT = Depends(get_session),
):
    new_data = data.dict(exclude_unset=True)
    if "grades" in new_data:
        grades_ids = [grade.id for grade in data.grades]
        new_data["grades"] = services.get_grades_by_ids(session, grades_ids)

    for attr, value in new_data.items():
        setattr(role, attr, value)

    session.add(role)
    session.commit()
    return role


@roles_router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: int,
    session: SessionT = Depends(get_session),
    crud: CRUD[models.Role] = Depends(get_roles_crud),
):
    ok = crud.delete_by_id(role_id)
    if not ok:
        raise_404(message=f"Role with id={role_id} not found")
    session.commit()


def get_grades_crud(session: SessionT = Depends(get_session)) -> CRUD[models.Grade]:
    return services.grades_crud_factory(session)


def valid_grade_id(grade_id: int, crud: CRUD[models.Grade] = Depends(get_grades_crud)) -> models.Grade:
    grade = crud.get_by_id(grade_id)
    if not grade:
        raise_404(message=f"Grade with id={grade_id} not found")
    return grade


@grades_router.get("/{grade_id}", response_model=schemas.GradeRead)
def get_grade(
    grade: models.Grade = Depends(valid_grade_id),
):
    return grade


@grades_router.get("", response_model=list[schemas.GradeRead])
def get_grades(
    crud: CRUD[models.Grade] = Depends(get_grades_crud),
):
    return crud.get_all()


@grades_router.post("", response_model=schemas.GradeRead, status_code=status.HTTP_201_CREATED)
def create_grade(
    data: schemas.GradeCreate,
    session: SessionT = Depends(get_session),
):
    grade = models.Grade(**data.dict())
    session.add(grade)
    session.commit()
    return grade


@grades_router.patch("/{grade_id}", response_model=schemas.GradeRead)
def update_grade(
    data: schemas.GradeUpdate,
    grade: models.Grade = Depends(valid_grade_id),
    session: SessionT = Depends(get_session),
):
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(grade, attr, value)

    session.add(grade)
    session.commit()
    return grade


@grades_router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(
    grade_id: int,
    session: SessionT = Depends(get_session),
    crud: CRUD[models.Grade] = Depends(get_grades_crud),
):
    ok = crud.delete_by_id(grade_id)
    if not ok:
        raise_404(message=f"Grade with id={grade_id} not found")
    session.commit()


def get_skills_crud(session: SessionT = Depends(get_session)) -> CRUD[models.Skill]:
    return services.skills_crud_factory(session)


def valid_skill_id(skill_id: int, crud: CRUD[models.Skill] = Depends(get_skills_crud)) -> models.Skill:
    skill = crud.get_by_id(skill_id)
    if not skill:
        raise_404(message=f"Skill with id={skill_id} not found")
    return skill


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
