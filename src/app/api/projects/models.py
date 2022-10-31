import typing as t
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.api.projects.constants import ProjectStatuses
from app.api.users.constants import UserTypes
from app.api.users.models import User
from app.core.db import (
    BaseModel,
    SurrogateKeyMixin,
    TimestampMixin,
    SoftDeleteMixin,
    StrSizes,
)

if t.TYPE_CHECKING:
    from app.api.employees.models import Employee

__all__ = [
    "Project",
    "ProjectOwner",
    "ProjectManager",
]


class Project(BaseModel, SurrogateKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "project"

    owner_id: int = sa.Column(sa.ForeignKey("user.id"), nullable=False)
    manager_id: int = sa.Column(sa.ForeignKey("user.id"))

    code: str = sa.Column(sa.String(StrSizes.XS), unique=True, nullable=False)
    name: str = sa.Column(sa.String(StrSizes.MD), nullable=False)

    status: ProjectStatuses = sa.Column(sa.Enum(ProjectStatuses), default=ProjectStatuses.default)

    start_date: datetime = sa.Column(sa.DateTime)
    end_date: datetime = sa.Column(sa.DateTime)

    contract_price: float = sa.Column(sa.Float)

    owner: "ProjectOwner" = relationship(
        "ProjectOwner",
        foreign_keys=[owner_id],
        back_populates="owned_projects",
    )
    manager: "ProjectManager" = relationship(
        "ProjectManager",
        foreign_keys=[manager_id],
        back_populates="managed_projects",
    )
    resources: list["Employee"] = relationship(
        "Employee",
        secondary="project_resource_link",
        back_populates="projects",
    )


# Single Table Inheritance - несколько типов классов представлены одной таблицей:
# https://docs.sqlalchemy.org/en/14/orm/inheritance.html#single-table-inheritance
class ProjectOwner(User):
    owned_projects: list["Project"] = relationship(
        "Project",
        foreign_keys="[Project.owner_id]",
        back_populates="owner",
    )

    __mapper_args__ = {
        "polymorphic_identity": UserTypes.project_owner,
    }


# Single Table Inheritance - несколько типов классов представлены одной таблицей:
# https://docs.sqlalchemy.org/en/14/orm/inheritance.html#single-table-inheritance
class ProjectManager(User):
    managed_projects: list["Project"] = relationship(
        "Project",
        foreign_keys="[Project.manager_id]",
        back_populates="manager",
    )

    __mapper_args__ = {
        "polymorphic_identity": UserTypes.project_manager,
    }
