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

    manager: "Employee" = relationship(
        "Employee",
        remote_side="Employee.id",
        back_populates="employees",
    )
    employees: list["Employee"] = relationship(
        "Employee",
        back_populates="manager",
    )

    role_grade_records: list["RoleGradeLink"] = relationship(
        "RoleGradeLink",
        secondary="employee_role_grade_link",
        back_populates="employees",
    )
    skill_records: list["EmployeeSkillLink"] = relationship(
        "EmployeeSkillLink",
        back_populates="employee",
    )

    projects: list["Project"] = relationship(
        "Project",
        secondary="project_resource_link",
        back_populates="resources",
    )

    __mapper_args__ = {
        "polymorphic_identity": UserTypes.employee,
    }


class BufModel(User):
    manager_id: int = sa.Column(sa.ForeignKey("user.id", ondelete="SET NULL"))
