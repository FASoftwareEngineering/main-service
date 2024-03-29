from sqlalchemy import sql

from app.api.career import models
from app.api.services import CRUD
from app.core.db import SessionT


def roles_crud_factory(session: SessionT) -> CRUD[models.Role]:
    return CRUD(session, models.Role)


def grades_crud_factory(session: SessionT) -> CRUD[models.Grade]:
    return CRUD(session, models.Grade)


def skills_crud_factory(session: SessionT) -> CRUD[models.Skill]:
    return CRUD(session, models.Skill)


def get_grades_by_ids(session: SessionT, ids: list[int]) -> list[models.Grade]:
    stmt = sql.select(models.Grade).where(models.Grade.id.in_(ids))
    return session.scalars(stmt).all()


def get_role_grade(session: SessionT, role_id: int, grade_id: int) -> models.RoleGradeLink | None:
    stmt = sql.select(models.RoleGradeLink).where(
        (models.RoleGradeLink.role_id == role_id) & (models.RoleGradeLink.grade_id == grade_id),
    )
    return session.scalar(stmt)
