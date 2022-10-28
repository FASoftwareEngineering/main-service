from sqlalchemy import sql

from app.api.services import CRUD
from app.core.db import SessionT
from app.api.projects import models, schemas


def crud_factory(session: SessionT) -> CRUD[models.Project]:
    return CRUD(session, models.Project)


def get_projects_by(
    session: SessionT,
    by_simple: schemas.ProjectFilterParams,
    by_complex: schemas.ProjectComplexFilterParams,
    offset: int,
    limit: int,
) -> tuple[list[models.Project], int]:
    param_to_column_map = {
        attribute: getattr(models.Project, attribute)
        for attribute in models.Project.__mapper__.column_attrs.keys()
    }

    clause = sql.true()
    for p, v in by_simple.dict(exclude_defaults=True).items():
        clause &= param_to_column_map[p] == v
    simple_filter_stmt = sql.select(models.Project).where(clause)  # type: ignore
    filter_stmt = simple_filter_stmt
    if by_complex.owner_id is not None:
        filter_stmt = filter_stmt.where(
            (
                models.OwnersProjectsLink.owner_id
                == by_complex.owner_id & models.OwnersProjectsLink.end_date.is_(None)
            )
        )
    if by_complex.manager_id is not None:
        filter_stmt = filter_stmt.where(
            (
                models.ManagersProjectsLink.manager_id
                == by_complex.manager_id & models.ManagersProjectsLink.end_date.is_(None)
            )
        )
    # TODO: add complex date/price filtration
    filter_stmt = filter_stmt.offset(offset).limit(limit)
    total = session.scalar(sql.select(sql.func.count()).select_from(filter_stmt))
    return session.scalars(filter_stmt).all(), total
