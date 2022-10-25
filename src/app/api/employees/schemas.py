from app.core.schemas import BaseSchema
from app.api.schemas import PaginationSchema
from app.api.users.constants import UserTypes


class EmployeeBase(BaseSchema):
    first_name: str
    last_name: str
    middle_name: str | None = None
    email: str | None = None
    phone: str | None = None


class EmployeeCreate(EmployeeBase):
    role: UserTypes = UserTypes.employee
    sso_id: int
    manager_id: int | None = None
    grades_to_roles_id: int | None = None


class EmployeeUpdate(EmployeeBase):
    first_name: str | None = None
    last_name: str | None = None
    manager_id: int | None = None
    grades_to_roles_id: int | None = None


class EmployeeRead(EmployeeBase):
    id: int


class EmployeePagination(PaginationSchema[EmployeeRead]):
    pass


class EmployeeFilterParams(BaseSchema):
    email: str | None = None
    phone: str | None = None
    manager_id: str | None = None
    first_name: str = None
    middle_name: str = None
    last_name: str = None


def valid_employee_filter_params(
    email: str = None,
    phone: str = None,
    manager_id: str = None,
    first_name: str = None,
    middle_name: str = None,
    last_name: str = None,
):
    # todo: role, grade, skills
    return EmployeeFilterParams(
        email=email,
        phone=phone,
        manager_id=manager_id,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
    )
