import typing as t

from fastapi import APIRouter, Depends, status
from pydantic import parse_obj_as

from app.api.constants import Prefixes, Tags
from app.api.employees.schemas import EmployeeFilterParams, valid_employee_filter_params
from app.api.exceptions import raise_404 as _raise_404
from app.api.services import CRUD
from app.api.dependencies import get_session, PaginationQuery, pagination_query
from app.api.employees import models
from app.api.employees import schemas, services
from app.core.db import SessionT

router = APIRouter(prefix=f"/{Prefixes.employees}", tags=[Tags.employees])


def raise_404(employee_id: int) -> t.NoReturn:
    _raise_404(message=f"Employee with id={employee_id} not found")


def get_crud(session: SessionT = Depends(get_session)) -> CRUD[models.Employee]:
    return services.crud_factory(session)


def valid_employee_id(employee_id: int, crud: CRUD[models.Employee] = Depends(get_crud)) -> models.Employee:
    employee = crud.get_by_id(employee_id)
    if not employee:
        raise_404(employee_id)
    return employee


@router.get("/{employee_id}", response_model=schemas.EmployeeRead)
def get_employee(
    employee: models.Employee = Depends(valid_employee_id),
):
    return employee


@router.get("", response_model=schemas.EmployeePagination)
def get_employees_with_pagination_and_filters(
    page_q: PaginationQuery = Depends(pagination_query),
    search_params_q: EmployeeFilterParams = Depends(valid_employee_filter_params),
    session: SessionT = Depends(get_session),
):
    employees, total = services.get_employees_by(session, search_params_q, page_q.offset, page_q.limit)
    return schemas.EmployeePagination(
        offset=page_q.offset,
        limit=page_q.limit,
        total=total,
        results=parse_obj_as(list[schemas.EmployeeRead], employees),
    )


@router.patch("/{employee_id}", response_model=schemas.EmployeeRead)
def update_employee(
    data: schemas.EmployeeUpdate,
    session: SessionT = Depends(get_session),
    employee: models.Employee = Depends(valid_employee_id),
    crud: CRUD[models.Employee] = Depends(get_crud),
):
    with session.begin():
        for attr, value in data.dict(exclude_unset=True).items():
            setattr(employee, attr, value)
        return crud.save(employee)


@router.post("", response_model=schemas.EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_employee(
    data: schemas.EmployeeCreate,
    session: SessionT = Depends(get_session),
    crud: CRUD[models.Employee] = Depends(get_crud),
):
    with session.begin():
        employee = models.Employee(**data.dict())
        return crud.save(employee)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    session: SessionT = Depends(get_session),
    crud: CRUD[models.Employee] = Depends(get_crud),
):
    with session.begin():
        ok = crud.delete_by_id(employee_id)
    if not ok:
        raise_404(employee_id)
