import typing as t

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.core.db import BaseModel, TimestampMixin

if t.TYPE_CHECKING:
    from app.api.career.models import Skill
    from app.api.employees.models import Employee

__all__ = [
    "EmployeeSkillLink",
    "ProjectResourceLink",
]


class EmployeeSkillLink(BaseModel, TimestampMixin):
    __tablename__ = "employee_skill_link"

    employee_id: int = sa.Column(sa.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    skill_id: int = sa.Column(sa.ForeignKey("skill.id", ondelete="CASCADE"), primary_key=True)

    score: int = sa.Column(sa.Integer, nullable=False)

    employee: "Employee" = relationship(
        "Employee",
        back_populates="skill_records",
    )
    skill: "Skill" = relationship(
        "Skill",
        back_populates="employee_records",
    )


class ProjectResourceLink(BaseModel, TimestampMixin):
    __tablename__ = "project_resource_link"

    project_id: int = sa.Column(sa.ForeignKey("project.id", ondelete="CASCADE"), primary_key=True)
    employee_id: int = sa.Column(sa.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
