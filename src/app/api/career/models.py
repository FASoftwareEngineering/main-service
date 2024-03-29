import typing as t

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.core.db import BaseModel, SoftDeleteMixin, StrSizes, SurrogateKeyMixin, TimestampMixin

if t.TYPE_CHECKING:
    from app.api.employees.models import Employee
    from app.api.models import EmployeeSkillLink

__all__ = [
    "Role",
    "Grade",
    "RoleGradeLink",
    "Skill",
]


class Role(BaseModel, SurrogateKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "role"

    name: str = sa.Column(sa.String(StrSizes.SM), unique=True, nullable=False)

    grades: list["Grade"] = relationship(
        "Grade",
        secondary="role_grade_link",
        back_populates="roles",
    )


class Grade(BaseModel, SurrogateKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "grade"

    name: str = sa.Column(sa.String(StrSizes.SM), unique=True, nullable=False)

    roles: list["Role"] = relationship(
        "Role",
        secondary="role_grade_link",
        back_populates="grades",
    )


class RoleGradeLink(BaseModel, SurrogateKeyMixin):
    __tablename__ = "role_grade_link"

    role_id: int = sa.Column(sa.ForeignKey("role.id", ondelete="CASCADE"), nullable=False)
    grade_id: int = sa.Column(sa.ForeignKey("grade.id", ondelete="CASCADE"), nullable=False)

    employees: list["Employee"] = relationship(
        "Employee",
        back_populates="role_grade",
    )

    __table_args__ = (sa.UniqueConstraint("role_id", "grade_id"),)


class Skill(BaseModel, SurrogateKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "skill"

    name: str = sa.Column(sa.String(StrSizes.SM), unique=True, nullable=False)
    max_score: int = sa.Column(sa.Integer, nullable=False)

    employee_records: list["EmployeeSkillLink"] = relationship(
        "EmployeeSkillLink",
        back_populates="skill",
    )
