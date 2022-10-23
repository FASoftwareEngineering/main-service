from datetime import datetime

import sqlalchemy as sa

from app.core.db import BaseModel

__all__ = [
    "OwnersProjectsLink",
    "ManagersProjectsLink",
]


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
