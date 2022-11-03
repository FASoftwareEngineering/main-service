from fastapi import APIRouter

from app.api import career, employees, projects, users

router = APIRouter(prefix="/v1", responses={404: {"description": "Not found"}})

router.include_router(users.router)

router.include_router(projects.router)

router.include_router(employees.router)

router.include_router(career.roles_router)
router.include_router(career.grades_router)
router.include_router(career.skills_router)
