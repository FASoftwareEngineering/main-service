from enum import Enum


class UserTypes(str, Enum):
    user = "user"
    employee = "employee"
    project_owner = "project_owner"
    project_manager = "project_manager"


class PublicUserTypes(str, Enum):
    employee = UserTypes.employee.value
    project_owner = UserTypes.project_owner.value
    project_manager = UserTypes.project_manager.value
