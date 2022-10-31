from enum import Enum


class Prefixes(str, Enum):
    users = "users"
    projects = "projects"
    employees = "employees"
    roles = "roles"
    grades = "grades"
    skills = "skills"


class Tags(str, Enum):
    users = "Users"
    projects = "Projects"
    employees = "Employees"
    roles = "Roles"
    grades = "Grades"
    skills = "Skills"
