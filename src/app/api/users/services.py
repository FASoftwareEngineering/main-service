from fastapi import HTTPException, status
from sqlalchemy import exc, sql

from app.api.services import CRUD
from app.api.users import models, schemas, constants
from app.core.db import SessionT


def crud_factory(session: SessionT) -> CRUD[models.User]:
    return CRUD(session, models.User)


def get_users_with_pagination_by(
    session: SessionT,
    by: schemas.UserFilterQuery,
    offset: int,
    limit: int,
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

    stmt = sql.select(models.User).where(clause).offset(offset).limit(limit)

    total = session.scalar(sql.select(sql.func.count()).select_from(stmt))
    return session.scalars(stmt).all(), total


def create_user(session: SessionT, data: schemas.UserCreate) -> models.User:
    if data.type == constants.PublicUserTypes.employee:
        return create_employee(session, data)

    user = models.User(**data.dict())
    try:
        session.add(user)
        session.commit()
    # TODO: создать свое исключение, обработать его во view
    except exc.IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"msg": e.orig.diag.message_detail},
        )
    return user


# TODO: подумать над реализацией более очевидного поведения
def create_employee(session: SessionT, data: schemas.UserCreate) -> models.User:
    user = get_employee_by_email(session, data.email)
    if user is None:
        user = models.User(**data.dict())
    else:
        user.sso_id = data.sso_id

    session.add(user)
    session.commit()
    return user


def get_employee_by_email(session: SessionT, email: str) -> models.User | None:
    stmt = sql.select(models.User).where(
        (models.User.type == constants.UserTypes.employee) & (models.User.email == email)
    )
    return session.scalar(stmt)
