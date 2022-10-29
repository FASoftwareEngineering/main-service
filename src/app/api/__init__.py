from fastapi import APIRouter

from app.api import projects, career, employees

router = APIRouter(prefix="/v1", responses={404: {"description": "Not found"}})

router.include_router(projects.router)
router.include_router(career.skills_router)
router.include_router(employees.router)
