import typing as t

from fastapi import APIRouter, Depends, status
from pydantic import parse_obj_as

from app.api.constants import Prefixes, Tags
from app.api.dependencies import PaginationQuery, get_session, pagination_query
from app.api.exceptions import raise_404 as _raise_404
from app.api.services import CRUD
from app.api.users import models, schemas, services
from app.core.db import SessionT

router = APIRouter(prefix=f"/{Prefixes.users}", tags=[Tags.users])


def raise_404(user_id: int) -> t.NoReturn:
    _raise_404(message=f"User with id={user_id} not found")


def get_crud(session: SessionT = Depends(get_session)) -> CRUD[models.User]:
    return services.crud_factory(session)


def valid_user_id(user_id: int, crud: CRUD[models.User] = Depends(get_crud)) -> models.User:
    user = crud.get_by_id(user_id)
    if not user:
        raise_404(user_id)
    return user


@router.get("/{user_id}", response_model=schemas.UserRead)
def get_user(
    user: models.User = Depends(valid_user_id),
):
    return user


@router.get("", response_model=schemas.UserPagination)
def get_users_with_pagination_and_filters(
    page_q: PaginationQuery = Depends(pagination_query),
    filter_q: schemas.UserFilterQuery = Depends(),
    session: SessionT = Depends(get_session),
):
    users, total = services.get_users_with_pagination_by(session, filter_q, page_q.offset, page_q.limit)
    return schemas.UserPagination(
        offset=page_q.offset,
        limit=page_q.limit,
        total=total,
        results=parse_obj_as(list[schemas.UserRead], users),
    )


@router.post("", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    current_data: schemas.UserCreate,
    session: SessionT = Depends(get_session),
):
    return services.create_user(session, current_data)


@router.patch("/{user_id}", response_model=schemas.UserRead)
def update_user(
    current_data: schemas.UserUpdate,
    user: models.User = Depends(valid_user_id),
    session: SessionT = Depends(get_session),
    crud: CRUD[models.User] = Depends(get_crud),
):
    with session.begin():
        for attr, current_value in current_data.dict(exclude_unset=True).items():
            setattr(user, attr, current_value)
        return crud.save(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    session: SessionT = Depends(get_session),
    crud: CRUD[models.User] = Depends(get_crud),
):
    with session.begin():
        ok = crud.delete_by_id(user_id)
    if not ok:
        raise_404(user_id)
