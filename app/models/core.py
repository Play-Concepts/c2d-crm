import uuid

from pydantic import BaseModel


class CoreModel(BaseModel):
    """
    Any common logic to be shared by all models goes here.
    """
    pass


class IDModelMixin(BaseModel):
    id: uuid.UUID


class CreatedCount(BaseModel):
    count: int
