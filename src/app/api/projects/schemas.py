from datetime import datetime

from pydantic import Field

from app.api.projects.constants import ProjectStatuses
from app.api.schemas import PaginationSchema
from app.core.schemas import BaseSchema


class ProjectEmployeeBase(BaseSchema):
    id: int
    first_name: str
    last_name: str
    middle_name: str | None = None
    email: str
    phone: str


class ProjectOwnerRead(ProjectEmployeeBase):
    pass


class ProjectManagerRead(ProjectEmployeeBase):
    pass


class ProjectResourceRead(ProjectEmployeeBase):
    pass


class ProjectBase(BaseSchema):
    code: str
    name: str
    status: ProjectStatuses
    start_date: datetime | None = None
    end_date: datetime | None = None
    contract_price: float | None = None


class ProjectCreate(ProjectBase):
    status: ProjectStatuses = ProjectStatuses.default

    owner_id: int
    manager_id: int | None = None
    resource_ids: list[int] = []


class ProjectUpdate(ProjectBase):
    code: str | None = None
    name: str | None = None
    status: ProjectStatuses | None = None

    owner_id: int | None = None
    manager_id: int | None = None
    resource_ids: list[int] = []


class ProjectRead(ProjectBase):
    id: int
    owner: ProjectOwnerRead
    manager: ProjectManagerRead | None = None
    resources: list[ProjectResourceRead]


class ProjectPagination(PaginationSchema[ProjectRead]):
    pass


class ProjectFilterQuery(BaseSchema):
    code: str | None = None
    name: str | None = None
    status: ProjectStatuses | None = None

    start_date: datetime | None = None
    start_date_gte: datetime | None = Field(default=None, alias="start_date__gte")
    start_date_lte: datetime | None = Field(default=None, alias="start_date__lte")

    end_date: datetime | None = None
    end_date_gte: datetime | None = Field(default=None, alias="end_date__gte")
    end_date_lte: datetime | None = Field(default=None, alias="end_date__lte")

    contract_price_gte: float | None = Field(default=None, alias="contract_price__gte")
    contract_price_lte: float | None = Field(default=None, alias="contract_price__lte")

    owner_id: int | None = None
    manager_id: int | None = None
