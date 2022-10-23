from datetime import datetime

from app.api.projects.constants import ProjectStatuses
from app.api.schemas import PaginationSchema
from app.core.schemas import BaseSchema


class ProjectBase(BaseSchema):
    code: str
    name: str
    status: ProjectStatuses
    start_date: datetime | None = None
    end_date: datetime | None = None
    contract_price: float | None = None


class ProjectCreate(ProjectBase):
    status: ProjectStatuses = ProjectStatuses.default


class ProjectUpdate(ProjectBase):
    code: str | None = None
    name: str | None = None
    status: ProjectStatuses | None = None


class ProjectRead(ProjectBase):
    id: int


class ProjectPagination(PaginationSchema[ProjectRead]):
    pass
