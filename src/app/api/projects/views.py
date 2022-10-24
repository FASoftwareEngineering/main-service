import typing as t

from fastapi import APIRouter, Depends, status
from pydantic import parse_obj_as

from app.api.constants import Prefixes, Tags
from app.api.dependencies import get_session, PaginationQuery, pagination_query
from app.api.exceptions import raise_404 as _raise_404
from app.api.projects import models, services, schemas
from app.api.services import CRUD
from app.core.db import SessionT

router = APIRouter(prefix=f"/{Prefixes.projects}", tags=[Tags.projects])


def raise_404(project_id: int) -> t.NoReturn:
    _raise_404(message=f"Project with id={project_id} not found")


def get_crud(session: SessionT = Depends(get_session)) -> CRUD[models.Project]:
    return services.crud_factory(session)


def valid_project_id(
    project_id: int, crud: CRUD[models.Project] = Depends(get_crud)
) -> models.Project:
    project = crud.get_by_id(project_id)
    if not project:
        raise_404(project_id)
    return project


@router.get("/{project_id}", response_model=schemas.ProjectRead)
def get_project(
    project: models.Project = Depends(valid_project_id),
):
    print(project.__dict__)  # Just for testing
    return project


@router.get("", response_model=schemas.ProjectPagination)
def get_projects(
    page_q: PaginationQuery = Depends(pagination_query),
    crud: CRUD[models.Project] = Depends(get_crud),
):
    projects, total = crud.get_all_paginate(offset=page_q.offset, limit=page_q.limit)
    return schemas.ProjectPagination(
        offset=page_q.offset,
        limit=page_q.limit,
        total=total,
        results=parse_obj_as(list[schemas.ProjectRead], projects),
    )


@router.post(
    "", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED
)
def create_project(
    data: schemas.ProjectCreate,
    session: SessionT = Depends(get_session),
    crud: CRUD[models.Project] = Depends(get_crud),
):
    with session.begin():
        project = models.Project(**data.dict())
        return crud.save(project)


@router.patch("/{project_id}", response_model=schemas.ProjectRead)
def update_project(
    data: schemas.ProjectUpdate,
    session: SessionT = Depends(get_session),
    project: models.Project = Depends(valid_project_id),
    crud: CRUD[models.Project] = Depends(get_crud),
):
    with session.begin():
        for attr, value in data.dict(exclude_unset=True).items():
            setattr(project, attr, value)
        return crud.save(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    session: SessionT = Depends(get_session),
    crud: CRUD[models.Project] = Depends(get_crud),
):
    with session.begin():
        ok = crud.delete_by_id(project_id)
    if not ok:
        raise_404(project_id)
