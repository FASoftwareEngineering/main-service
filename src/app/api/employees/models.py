import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.api.users.constants import UserTypes
from app.api.users.models import User

__all__ = [
    "Employee",
]


# Single Table Inheritance - несколько типов классов представлены одной таблицей:
# https://docs.sqlalchemy.org/en/14/orm/inheritance.html#single-table-inheritance
class Employee(User):
    manager_id: int = sa.Column(sa.ForeignKey("user.id", ondelete="SET NULL"))

    manager: "Employee" = relationship("Employee", remote_side="Employee.id", back_populates="employees")
    employees: list["Employee"] = relationship("Employee", back_populates="manager")

    __mapper_args__ = {
        "polymorphic_identity": UserTypes.employee,
    }
