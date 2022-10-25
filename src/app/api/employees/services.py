from sqlalchemy import sql

from app.api.employees import models
from app.api.employees.schemas import EmployeeFilterParams
from app.api.services import CRUD
from app.core.db import SessionT


def crud_factory(session: SessionT) -> CRUD[models.Employee]:
    return CRUD(session, models.Employee)


def get_employees_by(
    session: SessionT, by: EmployeeFilterParams, offset: int, limit: int
) -> tuple[list[models.Employee], int]:
    param_to_column_map = {
        "email": models.Employee.email,
        "phone": models.Employee.phone,
        "manager_id": models.Employee.manager_id,
        "last_name": models.Employee.last_name,
        "middle_name": models.Employee.middle_name,
        "first_name": models.Employee.first_name,
    }
    clause = sql.true()

    for p, v in by.dict(exclude_defaults=True).items():
        clause &= param_to_column_map[p] == v

    stmt = sql.select(models.Employee).where(clause).offset(offset).limit(limit)  # type: ignore
    total = session.scalar(sql.select(sql.func.count()).select_from(stmt))
    return session.scalars(stmt).all(), total
