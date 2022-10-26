from app.core.schemas import BaseSchema
from app.api.schemas import PaginationSchema


class EmployeeBase(BaseSchema):
    first_name: str
    last_name: str
    email: str
    phone: str
    middle_name: str | None = None


class EmployeeCreate(EmployeeBase):
    manager_id: int | None = None
    grades_to_roles_id: int | None = None


class EmployeeUpdate(EmployeeBase):
    first_name: str | None = None
    last_name: str | None = None
    manager_id: int | None = None
    email: str | None = None
    phone: str | None = None


class EmployeeRead(EmployeeBase):
    id: int


class EmployeePagination(PaginationSchema[EmployeeRead]):
    pass


class EmployeeFilterQuery(EmployeeBase):
    manager_id: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
