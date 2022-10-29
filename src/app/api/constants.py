from enum import Enum


class Prefixes(str, Enum):
    projects = "projects"
    employees = "employees"
    roles = "roles"
    grades = "grades"
    skills = "skills"


class Tags(str, Enum):
    projects = "Projects"
    employees = "Employees"
    roles = "Roles"
    grades = "Grades"
    skills = "Skills"
