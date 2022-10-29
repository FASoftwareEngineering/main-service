from sqlalchemy import sql

from app.api.projects import models, schemas
from app.api.services import CRUD
from app.core.db import SessionT


def crud_factory(session: SessionT) -> CRUD[models.Project]:
    return CRUD(session, models.Project)


def get_projects_with_pagination_by(
    session: SessionT,
    by: schemas.ProjectFilterQuery,
    offset: int,
    limit: int,
) -> tuple[list[models.Project], int]:
    clause = sql.true()

    param_column_eq_map = {
        "code": models.Project.code,
        "name": models.Project.name,
        "status": models.Project.status,
        "start_date": models.Project.start_date,
        "end_date": models.Project.end_date,
        "owner_id": models.Project.owner_id,
        "manager_id": models.Project.manager_id,
    }
    eq_params = by.dict(
        include=param_column_eq_map.keys(),
        exclude_unset=True,
        exclude_defaults=True,
    )
    for p, v in eq_params.items():
        clause &= param_column_eq_map[p] == v

    if by.start_date_lte is not None:
        clause &= models.Project.start_date <= by.start_date_lte
    if by.start_date_gte is not None:
        clause &= models.Project.start_date >= by.start_date_gte

    if by.end_date_lte is not None:
        clause &= models.Project.end_date <= by.end_date_lte
    if by.end_date_gte is not None:
        clause &= models.Project.end_date >= by.end_date_gte

    if by.contract_price_lte is not None:
        clause &= models.Project.contract_price <= by.contract_price_lte
    if by.contract_price_gte is not None:
        clause &= models.Project.contract_price >= by.contract_price_gte

    stmt = sql.select(models.Project).where(clause).offset(offset).limit(limit)  # type: ignore

    total = session.scalar(sql.select(sql.func.count()).select_from(stmt))
    return session.scalars(stmt).all(), total
