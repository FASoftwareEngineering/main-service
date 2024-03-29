from fastapi import Depends, Query

from app.api.schemas import PaginationSchema
from app.core.schemas import BaseSchema


class CareerRoleRead(BaseSchema):
    id: int
    name: str


class CareerGradeRead(BaseSchema):
    id: int
    name: str


class CareerSkillRead(BaseSchema):
    id: int
    name: str
    score: int
    max_score: int


class CareerSkillCreate(BaseSchema):
    id: int
    score: int


class CareerSkillUpdate(CareerSkillCreate):
    pass


class EmployeeManagerRead(BaseSchema):
    id: int
    first_name: str
    last_name: str
    middle_name: str | None = None
    email: str
    phone: str


class EmployeeBase(BaseSchema):
    first_name: str
    last_name: str
    middle_name: str | None = None
    email: str
    phone: str


class EmployeeCreate(EmployeeBase):
    manager_id: int | None = None
    role_id: int
    grade_id: int
    skills: list[CareerSkillCreate] = []


class EmployeeUpdate(EmployeeBase):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None

    manager_id: int | None = None
    role_id: int | None = None
    grade_id: int | None = None
    skills: list[CareerSkillUpdate] = []


class EmployeeRead(EmployeeBase):
    id: int
    manager: EmployeeManagerRead | None
    role: CareerRoleRead
    grade: CareerGradeRead
    skills: list[CareerSkillRead] = []


class EmployeePagination(PaginationSchema[EmployeeRead]):
    pass


class _EmployeeFilterQuery(BaseSchema):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None

    manager_id: int | None = None
    role_id: int | None = None
    grade_id: int | None = None


class EmployeeFilterQuery(_EmployeeFilterQuery):
    skill_ids: list[int] | None = None


# Список значений для параметра: ?param=1&param=2&param=3&...
# https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#query-parameter-list-multiple-values
def employee_filter_query(
    skill_ids: list[int] | None = Query(default=None, alias="skill_id"),
    filter_q: _EmployeeFilterQuery = Depends(),
) -> EmployeeFilterQuery:
    return EmployeeFilterQuery(**filter_q.dict(), skill_ids=skill_ids)
