import typing as t

from fastapi import APIRouter, status, Depends

from app.api.constants import Prefixes, Tags
from app.api.dependencies import get_session, PaginationQuery
from app.api.exceptions import raise_404 as _raise_404
from app.api.services import CRUD
from app.api.users import schemas, models, services
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
    page_q: PaginationQuery = Depends(),
    filter_q: schemas.UserFilterQuery = Depends(),
    session: SessionT = Depends(get_session),
):
    users, total = services.get_users_with_pagination_by(session, filter_q, page_q)
    return {
        "offset": page_q.offset,
        "limit": page_q.limit,
        "total": total,
        "results": users,
    }


@router.post("", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    data: schemas.UserCreate,
    session: SessionT = Depends(get_session),
):
    return services.create_user(session, data)


@router.patch("/{user_id}", response_model=schemas.UserRead)
def update_user(
    data: schemas.UserUpdate,
    user: models.User = Depends(valid_user_id),
    session: SessionT = Depends(get_session),
):
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(user, attr, value)

    session.add(user)
    session.commit()
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    session: SessionT = Depends(get_session),
    crud: CRUD[models.User] = Depends(get_crud),
):
    ok = crud.delete_by_id(user_id)
    if not ok:
        raise_404(user_id)
    session.commit()
