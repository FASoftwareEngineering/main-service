from pydantic import BaseModel

__all__ = [
    "BaseSchema",
]


class BaseSchema(BaseModel):
    """Базовый объект БД

    Базовый объект, от которого наследуются все остальные объекты
    """

    class Config:
        """Переопределение конфигурации"""

        orm_mode = True
