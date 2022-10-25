from enum import Enum


class Prefixes(str, Enum):
    projects = "projects"
    employees = "employees"
    skills = "skills"


class Tags(str, Enum):
    projects = "Projects"
    employees = "Employees"
    skills = "Skills"
