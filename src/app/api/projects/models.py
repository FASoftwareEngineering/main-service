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

__all__ = [
    "Project",
    "ProjectOwner",
    "ProjectManager",
    "OwnersProjectsLink",
    "ManagersProjectsLink",
]


class Project(BaseModel, SurrogateKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "project"

    code: str = sa.Column(sa.String(StrSizes.XS), unique=True, nullable=False)
    name: str = sa.Column(sa.String(StrSizes.MD), nullable=False)

    status: ProjectStatuses = sa.Column(sa.Enum(ProjectStatuses))

    start_date: datetime = sa.Column(sa.DateTime)
    end_date: datetime = sa.Column(sa.DateTime)

    contract_price: float = sa.Column(sa.Float)

    owners: list["ProjectOwner"] = relationship(
        "ProjectOwner",
        secondary="owners_projects_link",
        back_populates="owned_projects",
    )
    managers: list["ProjectManager"] = relationship(
        "ProjectManager",
        secondary="managers_projects_link",
        back_populates="managed_projects",
    )


# Single Table Inheritance - несколько типов классов представлены одной таблицей:
# https://docs.sqlalchemy.org/en/14/orm/inheritance.html#single-table-inheritance
class ProjectOwner(User):
    owned_projects: list["Project"] = relationship(
        "Project",
        secondary="owners_projects_link",
        back_populates="owners",
    )

    __mapper_args__ = {
        "polymorphic_identity": UserTypes.project_owner,
    }


# Single Table Inheritance - несколько типов классов представлены одной таблицей:
# https://docs.sqlalchemy.org/en/14/orm/inheritance.html#single-table-inheritance
class ProjectManager(User):
    managed_projects: list["Project"] = relationship(
        "Project",
        secondary="managers_projects_link",
        back_populates="managers",
    )

    __mapper_args__ = {
        "polymorphic_identity": UserTypes.project_manager,
    }


class OwnersProjectsLink(BaseModel):
    __tablename__ = "owners_projects_link"

    project_id: int = sa.Column(sa.ForeignKey("project.id", ondelete="CASCADE"), primary_key=True)
    owner_id: int = sa.Column(sa.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)

    start_date: datetime = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)
    end_date: datetime = sa.Column(sa.DateTime)


class ManagersProjectsLink(BaseModel):
    __tablename__ = "managers_projects_link"

    project_id: int = sa.Column(sa.ForeignKey("project.id", ondelete="CASCADE"), primary_key=True)
    manager_id: int = sa.Column(sa.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)

    start_date: datetime = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)
    end_date: datetime = sa.Column(sa.DateTime)
