from fastapi import APIRouter, status, Depends

from app.api.constants import Prefixes, Tags
from app.api.users import schemas

router = APIRouter(prefix=f"/{Prefixes.users}", tags=[Tags.users])


@router.get("/{user_id}", response_model=schemas.UserRead)
def get_user(
    user_id: int,
):
    pass


@router.get("", response_model=list[schemas.UserRead])
def get_users_with_filters(
    filter_q: schemas.UserFilterQuery = Depends(),
):
    pass


@router.post("", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    data: schemas.UserCreate,
):
    pass


@router.patch("/{user_id}", response_model=schemas.UserRead)
def update_user(
    user_id: int,
):
    pass


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
):
    pass
