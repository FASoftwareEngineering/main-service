from datetime import datetime

import typer
from sqlalchemy import sql

from app.api.career.models import Grade, Role, RoleGradeLink, Skill
from app.api.employees.models import Employee
from app.api.models import EmployeeSkillLink
from app.api.projects.constants import ProjectStatuses
from app.api.projects.models import Project, ProjectManager, ProjectOwner
from app.core.db import BaseModel, SessionLocal, SessionT, engine

app = typer.Typer()


@app.command(name="init-dev")
def init_dev(projects: bool = True, employees: bool = True) -> None:
    _clear()
    session = SessionLocal()

    if projects:
        _create_projects(session)
    if employees:
        _create_employees(session)


@app.command()
def clear() -> None:
    _clear()


def _create_projects(session: SessionT) -> None:
    project_owners = [
        ProjectOwner(
            sso_id="project_owner_1",
            email="project_owner_1@mail.ru",
            phone="+79999999999",
            first_name="Иван",
            last_name="Иванов",
        ),
        ProjectOwner(
            sso_id="project_owner_2",
            email="project_owner_2@mail.ru",
            phone="+78888888888",
            first_name="Петр",
            last_name="Петров",
        ),
    ]
    project_managers = [
        ProjectManager(
            sso_id="project_manager_1",
            email="project_manager_1@mail.ru",
            phone="+77777777777",
            first_name="София",
            last_name="Круглова",
        ),
        ProjectManager(
            sso_id="project_manager_2",
            email="project_manager_2@mail.ru",
            phone="+76666666666",
            first_name="Лев",
            last_name="Попов",
        ),
    ]
    projects = [
        Project(
            code="PROJ_1",
            name="Проект 1",
        ),
        Project(
            code="PROJ_2",
            name="Проект 2",
            status=ProjectStatuses.active,
            start_date=datetime(2022, 10, 31),
            end_date=datetime(2024, 12, 12),
            contract_price=6_000_000,
        ),
    ]

    for project, owner, manager in zip(projects, project_owners, project_managers):
        project.owner = owner
        project.manager = manager

    session.add_all([*projects, *project_owners, *project_managers])
    session.commit()


def _create_employees(session: SessionT) -> None:
    skills = {
        "python": Skill(name="python", max_score=3),
        "fastapi": Skill(name="fastapi", max_score=3),
        "flask": Skill(name="flask", max_score=3),
        "django": Skill(name="django", max_score=3),
        "postgresql": Skill(name="postgresql", max_score=3),
        "postman": Skill(name="postman", max_score=2),
        "pytest": Skill(name="pytest", max_score=2),
        "unittest": Skill(name="unittest", max_score=2),
        "jira": Skill(name="jira", max_score=2),
        "confluence": Skill(name="confluence", max_score=2),
        "miro": Skill(name="miro", max_score=2),
        "uml": Skill(name="uml", max_score=2),
        "erd": Skill(name="erd", max_score=2),
    }
    grades = [
        Grade(name="младший"),
        Grade(name="старший"),
        Grade(name="junior"),
        Grade(name="middle"),
        Grade(name="senior"),
    ]
    roles = [
        Role(name="менеджер практики", grades=grades[:2]),
        Role(name="аналитик", grades=grades[:2]),
        Role(name="архитектор", grades=grades[2:]),
        Role(name="разработчик", grades=grades[2:]),
        Role(name="тестировщик", grades=grades[2:]),
    ]
    session.add_all([*roles, *grades, *skills.values()])
    session.flush([*roles, *grades, *skills.values()])

    role_grade_records = {
        "manager1": _get_role_grade(session, roles[0], roles[0].grades[1]),
        "manager2": _get_role_grade(session, roles[0], roles[0].grades[1]),
        "analyst": _get_role_grade(session, roles[1], roles[1].grades[1]),
        "architect": _get_role_grade(session, roles[2], roles[2].grades[2]),
        "developer1": _get_role_grade(session, roles[3], roles[3].grades[2]),
        "developer2": _get_role_grade(session, roles[3], roles[3].grades[1]),
        "developer3": _get_role_grade(session, roles[3], roles[3].grades[0]),
        "tester": _get_role_grade(session, roles[4], roles[4].grades[0]),
    }
    skill_records = {
        "analyst": [
            EmployeeSkillLink(skill=skills["jira"], score=2),
            EmployeeSkillLink(skill=skills["confluence"], score=2),
        ],
        "architect": [
            EmployeeSkillLink(skill=skills["miro"], score=1),
            EmployeeSkillLink(skill=skills["uml"], score=2),
            EmployeeSkillLink(skill=skills["erd"], score=2),
        ],
        "developer1": [
            EmployeeSkillLink(skill=skills["python"], score=3),
            EmployeeSkillLink(skill=skills["fastapi"], score=1),
            EmployeeSkillLink(skill=skills["flask"], score=2),
            EmployeeSkillLink(skill=skills["django"], score=1),
            EmployeeSkillLink(skill=skills["postgresql"], score=2),
        ],
        "developer2": [
            EmployeeSkillLink(skill=skills["python"], score=3),
            EmployeeSkillLink(skill=skills["fastapi"], score=1),
            EmployeeSkillLink(skill=skills["flask"], score=2),
            EmployeeSkillLink(skill=skills["django"], score=1),
            EmployeeSkillLink(skill=skills["postgresql"], score=2),
        ],
        "developer3": [
            EmployeeSkillLink(skill=skills["python"], score=3),
            EmployeeSkillLink(skill=skills["fastapi"], score=1),
            EmployeeSkillLink(skill=skills["flask"], score=2),
            EmployeeSkillLink(skill=skills["django"], score=1),
            EmployeeSkillLink(skill=skills["postgresql"], score=2),
        ],
        "tester": [
            EmployeeSkillLink(skill=skills["postman"], score=2),
            EmployeeSkillLink(skill=skills["pytest"], score=1),
            EmployeeSkillLink(skill=skills["unittest"], score=0),
        ],
    }

    managers = [
        Employee(
            sso_id="employee_manager_1",
            email="employee_manager_1@mail.ru",
            phone="+75555555555",
            first_name="Марк",
            last_name="Григорьев",
            role_grade=role_grade_records["manager1"],
        ),
        Employee(
            sso_id="employee_manager_2",
            email="employee_manager_2@mail.ru",
            phone="+74444444444",
            first_name="Анна",
            last_name="Фролова",
            role_grade=role_grade_records["manager2"],
        ),
    ]
    employees = [
        [
            Employee(
                sso_id="employee_1",
                email="employee_1@mail.ru",
                phone="+73333333333",
                first_name="Анна",
                last_name="Платонова",
                role_grade=role_grade_records["analyst"],
                skill_records=skill_records["analyst"],
            ),
            Employee(
                sso_id="employee_2",
                email="employee_2@mail.ru",
                phone="+72222222222",
                first_name="Мария",
                last_name="Чернышева",
                role_grade=role_grade_records["architect"],
                skill_records=skill_records["architect"],
            ),
            Employee(
                sso_id="employee_3",
                email="employee_3@mail.ru",
                phone="+71111111111",
                first_name="Мария",
                last_name="Маркова",
                role_grade=role_grade_records["developer1"],
                skill_records=skill_records["developer1"],
            ),
            Employee(
                sso_id="employee_4",
                email="employee_4@mail.ru",
                phone="+79879879898",
                first_name="Иван",
                last_name="Тихонов",
                role_grade=role_grade_records["developer2"],
                skill_records=skill_records["developer2"],
            ),
        ],
        [
            Employee(
                sso_id="employee_5",
                email="employee_5@mail.ru",
                phone="+78768769797",
                first_name="Мирон",
                last_name="Иванов",
                role_grade=role_grade_records["developer3"],
                skill_records=skill_records["developer3"],
            ),
            Employee(
                sso_id="employee_6",
                email="employee_6@mail.ru",
                phone="+776576567676",
                first_name="Полина",
                last_name="Романова",
                role_grade=role_grade_records["tester"],
                skill_records=skill_records["tester"],
            ),
        ],
    ]

    for manager, es in zip(managers, employees):
        manager.employees = es

    session.add_all([*managers, *[e for es in employees for e in es]])
    session.commit()


def _get_role_grade(session: SessionT, role: Role, grade: Grade) -> RoleGradeLink | None:
    stmt = sql.select(RoleGradeLink).where(
        (RoleGradeLink.role_id == role.id) & (RoleGradeLink.grade_id == grade.id)
    )
    return session.scalar(stmt)


def _clear() -> None:
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)
