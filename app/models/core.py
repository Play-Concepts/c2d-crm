import json
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


Count = CreatedCount


class BooleanResponse(BaseModel):
    value: bool


class NotFound(BaseModel):
    message: str


class InvalidToken(BaseModel):
    message: str


def decode_json(cls, v):
    if not isinstance(v, str):
        try:
            return json.dumps(v)
        except Exception as err:
            raise ValueError(f"Could not parse value into valid JSON: {err}")

    return v
