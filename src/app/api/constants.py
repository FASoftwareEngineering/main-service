from enum import Enum


class Prefixes(str, Enum):
    projects = "projects"
    employees = "employees"
    skills = "skills"
    levels = 'levels'


class Tags(str, Enum):
    projects = "Projects"
    employees = "Employees"
    skills = "Skills"
    level = "Levels"
