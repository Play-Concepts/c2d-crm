import uuid
from typing import Optional

from pydantic import BaseModel


class CoreModel(BaseModel):
    """
    Any common logic to be shared by all models goes here.
    """
    pass


class IDModelMixin(BaseModel):
    id: Optional[uuid.UUID]


class CreatedCount(BaseModel):
    count: int


class NotFound(BaseModel):
    message: str
