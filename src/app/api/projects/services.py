from app.api.projects import models
from app.api.services import CRUD
from app.core.db import SessionT


def crud_factory(session: SessionT) -> CRUD[models.Project]:
    return CRUD(session, models.Project)
