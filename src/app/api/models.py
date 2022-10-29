import sqlalchemy as sa

from app.core.db import BaseModel, TimestampMixin

__all__ = [
    "EmployeeRoleGradeLink",
    "EmployeeSkillLink",
]


class EmployeeRoleGradeLink(BaseModel, TimestampMixin):
    __tablename__ = "employee_role_grade_link"

    employee_id: int = sa.Column(sa.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    role_grade_id: int = sa.Column(sa.ForeignKey("role_grade_link.id", ondelete="CASCADE"), primary_key=True)


class EmployeeSkillLink(BaseModel, TimestampMixin):
    __tablename__ = "employee_skill_link"

    employee_id: int = sa.Column(sa.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    skill_id: int = sa.Column(sa.ForeignKey("skill.id", ondelete="CASCADE"), primary_key=True)

    score: int = sa.Column(sa.Integer, nullable=False)
