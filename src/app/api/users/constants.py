from enum import Enum


class UserTypes(str, Enum):
    user = "user"
    employee = "employee"
    manager = "manager"
    project_owner = "project_owner"
    project_manager = "project_manager"
