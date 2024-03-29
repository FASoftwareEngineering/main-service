from sqlalchemy import sql

from app.api.dependencies import PaginationQuery
from app.api.projects import models, schemas
from app.api.services import CRUD, count_rows
from app.core.db import SessionT


def crud_factory(session: SessionT) -> CRUD[models.Project]:
    return CRUD(session, models.Project)


def get_projects_with_pagination_by(
    session: SessionT,
    by: schemas.ProjectFilterQuery,
    page_q: PaginationQuery,
) -> tuple[list[models.Project], int]:
    clause = sql.true()

    param_col_eq_map = {
        "code": models.Project.code,
        "name": models.Project.name,
        "status": models.Project.status,
        "start_date": models.Project.start_date,
        "end_date": models.Project.end_date,
        "owner_id": models.Project.owner_id,
        "manager_id": models.Project.manager_id,
    }
    eq_params = by.dict(
        include=param_col_eq_map.keys(),
        exclude_unset=True,
        exclude_defaults=True,
    )
    for p, v in eq_params.items():
        clause &= param_col_eq_map[p] == v

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

    stmt = sql.select(models.Project).where(clause).offset(page_q.offset).limit(page_q.limit)
    return session.scalars(stmt).all(), count_rows(session, stmt)
