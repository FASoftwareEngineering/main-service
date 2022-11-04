import typing as t

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.api.users.constants import UserTypes
from app.api.users.models import User

if t.TYPE_CHECKING:
    from app.api.career.models import RoleGradeLink
    from app.api.models import EmployeeSkillLink
    from app.api.projects.models import Project

__all__ = [
    "Employee",
]


# Single Table Inheritance - несколько типов классов представлены одной таблицей:
# https://docs.sqlalchemy.org/en/14/orm/inheritance.html#single-table-inheritance
class Employee(User):
    manager_id: int = sa.Column(sa.ForeignKey("user.id", ondelete="SET NULL"))
    role_grade_id: int = sa.Column(sa.ForeignKey("role_grade_link.id"))

    manager: "Employee" = relationship(
        "Employee",
        remote_side="Employee.id",
        back_populates="employees",
    )
    employees: list["Employee"] = relationship(
        "Employee",
        back_populates="manager",
    )

    role_grade: "RoleGradeLink" = relationship(
        "RoleGradeLink",
        back_populates="employees",
    )

    # https://stackoverflow.com/questions/23699651/dependency-rule-tried-to-blank-out-primary-key-in-sqlalchemy-when-foreign-key-c
    skill_records: list["EmployeeSkillLink"] = relationship(
        "EmployeeSkillLink",
        back_populates="employee",
        cascade="save-update, merge, delete, delete-orphan",
    )

    projects: list["Project"] = relationship(
        "Project",
        secondary="project_resource_link",
        back_populates="resources",
    )

    __mapper_args__ = {
        "polymorphic_identity": UserTypes.employee,
    }
