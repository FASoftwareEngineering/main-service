from sqlalchemy import sql

from app.api.career.models import RoleGradeLink
from app.api.dependencies import PaginationQuery
from app.api.employees import models, schemas
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

    stmt = stmt.where(clause).offset(page_q.offset).limit(page_q.limit)
    return session.scalars(stmt).all(), count_rows(session, stmt)


def get_employees_by_ids(session: SessionT, ids: list[int]) -> list[models.Employee]:
    stmt = sql.select(models.Employee).where(models.Employee.id.in_(ids))
    return session.scalars(stmt).all()
