from fastapi import APIRouter

from app.api import projects, employees

router = APIRouter(prefix="/v1", responses={404: {"description": "Not found"}})

router.include_router(projects.router)
router.include_router(employees.router)
