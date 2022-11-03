import typing as t

from sqlalchemy import sql

from app.api.career.models import Grade, Role, RoleGradeLink
from app.api.dependencies import PaginationQuery
from app.api.employees import models, schemas
from app.api.models import EmployeeSkillLink
from app.api.services import CRUD, count_rows
from app.core.db import SessionT


def crud_factory(session: SessionT) -> CRUD[models.Employee]:
    return CRUD(session, models.Employee)


def get_employees_with_pagination_by(
    session: SessionT,
    by: schemas.EmployeeFilterQuery,
    page_q: PaginationQuery,
) -> tuple[list[models.Employee], int]:
    clause = sql.true()

    param_col_eq_map = {
        "first_name": models.Employee.first_name,
        "last_name": models.Employee.last_name,
        "email": models.Employee.email,
        "phone": models.Employee.phone,
        "manager_id": models.Employee.manager_id,
    }
    eq_params = by.dict(
        include=param_col_eq_map.keys(),
        exclude_unset=True,
        exclude_defaults=True,
    )
    for p, v in eq_params.items():
        clause &= param_col_eq_map[p] == v

    stmt = sql.select(models.Employee)

    if by.role_id is not None or by.grade_id is not None:
        stmt = stmt.join(RoleGradeLink)
        if by.role_id is not None:
            clause &= RoleGradeLink.role_id == by.role_id
        if by.grade_id is not None:
            clause &= RoleGradeLink.grade_id == by.grade_id

    if by.skill_ids:
        stmt = stmt.join(EmployeeSkillLink)
        # FIXME: как записать на SQL'ном: отобрать всех сотрудников,
        #  у которых есть все навыки из by.skill_ids?
        clause &= EmployeeSkillLink.skill_id.in_(by.skill_ids)

    stmt = stmt.where(clause).offset(page_q.offset).limit(page_q.limit)
    return session.scalars(stmt).all(), count_rows(session, stmt)


def get_employees_by_ids(session: SessionT, ids: list[int]) -> list[models.Employee]:
    stmt = sql.select(models.Employee).where(models.Employee.id.in_(ids))
    return session.scalars(stmt).all()


def get_employee_by_email(session: SessionT, email: str) -> models.Employee | None:
    stmt = sql.select(models.Employee).where(models.Employee.email == email)
    return session.scalar(stmt)


def employee_exists(session: SessionT, id_: int) -> bool:
    stmt = sql.select(models.Employee.id).where(models.Employee.id == id_)
    return session.scalar(stmt) is not None


def employee_to_schema_read(session: SessionT, employee: models.Employee) -> dict[str, t.Any]:
    role = session.get(Role, employee.role_grade.role_id)
    grade = session.get(Grade, employee.role_grade.grade_id)
    skills = []
    for record in employee.skill_records:
        skills.append(
            {
                "id": record.skill.id,
                "name": record.skill.name,
                "score": record.score,
                "max_score": record.skill.max_score,
            },
        )

    return {
        "id": employee.id,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "middle_name": employee.middle_name,
        "email": employee.email,
        "phone": employee.phone,
        "manager": employee.manager,
        "role": role,
        "grade": grade,
        "skills": skills,
    }
