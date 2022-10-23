from enum import Enum


class Prefixes(str, Enum):
    projects = "projects"
    employees = "employees"


class Tags(str, Enum):
    projects = "Projects"
    employees = "Employees"
