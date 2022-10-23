from pydantic import BaseModel

__all__ = [
    "BaseSchema",
]


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
