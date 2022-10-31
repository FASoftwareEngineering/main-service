import typing as t

from fastapi import APIRouter, Depends, status

from app.api.constants import Prefixes, Tags
from app.api.dependencies import get_session, PaginationQuery
from app.api.employees.services import get_employees_by_ids
from app.api.exceptions import raise_404 as _raise_404
from app.api.projects import models, services, schemas
from app.api.services import CRUD
from app.core.db import SessionT

router = APIRouter(prefix=f"/{Prefixes.projects}", tags=[Tags.projects])


def raise_404(project_id: int) -> t.NoReturn:
    _raise_404(message=f"Project with id={project_id} not found")


def get_crud(session: SessionT = Depends(get_session)) -> CRUD[models.Project]:
    return services.crud_factory(session)


def valid_project_id(project_id: int, crud: CRUD[models.Project] = Depends(get_crud)) -> models.Project:
    project = crud.get_by_id(project_id)
    if not project:
        raise_404(project_id)
    return project


@router.get("/{project_id}", response_model=schemas.ProjectRead)
def get_project(
    project: models.Project = Depends(valid_project_id),
):
    return project


@router.get("", response_model=schemas.ProjectPagination)
def get_projects_with_pagination_and_filters(
    page_q: PaginationQuery = Depends(),
    filter_q: schemas.ProjectFilterQuery = Depends(),
    session: SessionT = Depends(get_session),
):
    projects, total = services.get_projects_with_pagination_by(session, filter_q, page_q)
    return {
        "offset": page_q.offset,
        "limit": page_q.limit,
        "total": total,
        "results": projects,
    }


@router.post("", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    data: schemas.ProjectCreate,
    session: SessionT = Depends(get_session),
    crud: CRUD[models.Project] = Depends(get_crud),
):
    new_data = data.dict()
    resource_ids = [res.id for res in data.resources]
    new_data["resources"] = get_employees_by_ids(session, resource_ids)

    project = models.Project(**new_data)
    return crud.save(project)


@router.patch("/{project_id}", response_model=schemas.ProjectRead)
def update_project(
    data: schemas.ProjectUpdate,
    project: models.Project = Depends(valid_project_id),
    session: SessionT = Depends(get_session),
    crud: CRUD[models.Project] = Depends(get_crud),
):
    new_data = data.dict(exclude_unset=True)
    if "resources" in new_data:
        resource_ids = [res.id for res in data.resources]
        new_data["resources"] = get_employees_by_ids(session, resource_ids)

    for attr, value in new_data.items():
        setattr(project, attr, value)

    return crud.save(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    session: SessionT = Depends(get_session),
    crud: CRUD[models.Project] = Depends(get_crud),
):
    ok = crud.delete_by_id(project_id)
    if not ok:
        raise_404(project_id)
    session.commit()
