from fastapi import HTTPException, status
from sqlalchemy import exc, sql

from app.api.dependencies import PaginationQuery
from app.api.services import CRUD, count_rows
from app.api.users import models, schemas, constants
from app.core.db import SessionT


def crud_factory(session: SessionT) -> CRUD[models.User]:
    return CRUD(session, models.User)


def get_users_with_pagination_by(
    session: SessionT,
    by: schemas.UserFilterQuery,
    page_q: PaginationQuery,
) -> tuple[list[models.User], int]:
    param_col_eq_map = {
        "type": models.User.type,
        "sso_id": models.User.sso_id,
        "email": models.User.email,
        "phone": models.User.phone,
        "first_name": models.User.first_name,
        "last_name": models.User.last_name,
    }
    eq_params = by.dict(
        include=param_col_eq_map.keys(),
        exclude_unset=True,
        exclude_defaults=True,
    )

    clause = sql.true()
    for p, v in eq_params.items():
        clause &= param_col_eq_map[p] == v

    stmt = sql.select(models.User).where(clause).offset(page_q.offset).limit(page_q.limit)
    return session.scalars(stmt).all(), count_rows(session, stmt)


def create_user(session: SessionT, data: schemas.UserCreate) -> models.User:
    if data.type == constants.PublicUserTypes.employee:
        return create_employee(session, data)

    try:
        crud = crud_factory(session)
        user = models.User(**data.dict())
        return crud.save(user)
    # TODO: создать свое исключение, обработать его во view
    except exc.IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"msg": e.orig.diag.message_detail},
        )


# TODO: подумать над реализацией более очевидного поведения
def create_employee(session: SessionT, data: schemas.UserCreate) -> models.User:
    user = get_employee_by_email(session, data.email)
    if user is None:
        user = models.User(**data.dict())
    else:
        user.sso_id = data.sso_id

    crud = crud_factory(session)
    return crud.save(user)


def get_employee_by_email(session: SessionT, email: str) -> models.User | None:
    stmt = sql.select(models.User).where(
        (models.User.type == constants.UserTypes.employee) & (models.User.email == email)
    )
    return session.scalar(stmt)
