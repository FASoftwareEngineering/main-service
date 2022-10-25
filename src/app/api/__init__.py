from fastapi import APIRouter

from app.api import projects, employees, career

router = APIRouter(prefix="/v1", responses={404: {"description": "Not found"}})

router.include_router(projects.router)
router.include_router(employees.router)
router.include_router(career.skills_router)
