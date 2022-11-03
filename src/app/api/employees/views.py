import typing as t

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import exc

from app.api.career.services import get_role_grade
from app.api.constants import Prefixes, Tags
from app.api.dependencies import PaginationQuery, get_session
from app.api.employees import models, schemas, services
from app.api.exceptions import raise_404 as _raise_404
from app.api.models import EmployeeSkillLink
from app.api.services import CRUD
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
    session: SessionT = Depends(get_session),
):
    return services.employee_to_schema_read(session, employee)


@router.get("", response_model=schemas.EmployeePagination)
def get_employees_with_pagination_and_filters(
    page_q: PaginationQuery = Depends(),
    filter_q: schemas.EmployeeFilterQuery = Depends(schemas.employee_filter_query),
    session: SessionT = Depends(get_session),
):
    employees, total = services.get_employees_with_pagination_by(session, filter_q, page_q)
    employees = [services.employee_to_schema_read(session, e) for e in employees]
    return {
        "offset": page_q.offset,
        "limit": page_q.limit,
        "total": total,
        "results": employees,
    }


@router.post("", response_model=schemas.EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_employee(
    data: schemas.EmployeeCreate,
    session: SessionT = Depends(get_session),
    crud: CRUD[models.Employee] = Depends(get_crud),
):
    role_grade = get_role_grade(session, data.role_id, data.grade_id)
    if role_grade is None:
        _raise_404(f"Record with role_id={data.role_id}, grade_id={data.role_id} not found")

    skill_records = []
    for skill in data.skills:
        skill_records.append(EmployeeSkillLink(skill_id=skill.id, score=skill.score))

    new_data = data.dict(exclude={"role_id", "grade_id", "skills"})
    new_data["role_grade"] = role_grade
    new_data["skill_records"] = skill_records

    if not services.employee_exists(session, data.manager_id):
        _raise_404(f"Manager with id={data.manager_id} not found")

    employee = services.get_employee_by_email(session, data.email)
    if employee is None:
        employee = models.Employee(**new_data)
    else:
        for attr, value in new_data.items():
            setattr(employee, attr, value)

    try:
        employee = crud.save(employee)
        return services.employee_to_schema_read(session, employee)
    except exc.IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"msg": e.orig.diag.message_detail},
        )


@router.patch("/{employee_id}", response_model=schemas.EmployeeRead)
def update_employee(
    data: schemas.EmployeeUpdate,
    employee: models.Employee = Depends(valid_employee_id),
    session: SessionT = Depends(get_session),
    crud: CRUD[models.Employee] = Depends(get_crud),
):
    new_data = data.dict(exclude_unset=True)

    if "role_id" in new_data or "grade_id" in new_data:
        role_id = new_data.pop("role_id", employee.role_grade.role_id)
        grade_id = new_data.pop("grade_id", employee.role_grade.grade_id)
        role_grade = get_role_grade(session, role_id, grade_id)
        if role_grade is None:
            _raise_404(f"Record with role_id={data.role_id}, grade_id={data.role_id} not found")
        employee.role_grade = role_grade

    if "skills" in new_data:
        skill_records = []
        for skill in new_data.pop("skills"):
            skill_records.append(EmployeeSkillLink(skill_id=skill.id, score=skill.score))
        employee.skill_records = skill_records

    for attr, value in new_data.items():
        setattr(employee, attr, value)

    try:
        employee = crud.save(employee)
        session.refresh(employee)
        return services.employee_to_schema_read(session, employee)
    except exc.IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"msg": e.orig.diag.message_detail},
        )


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    session: SessionT = Depends(get_session),
    crud: CRUD[models.Employee] = Depends(get_crud),
):
    ok = crud.delete_by_id(employee_id)
    if not ok:
        raise_404(employee_id)
    session.commit()
