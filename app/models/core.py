import json
import uuid
from datetime import datetime
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


class CreatedAtMixin(BaseModel):
    created_at: datetime


class UpdatedAtMixin(BaseModel):
    updated_at: datetime


class DaySeriesUnit(BaseModel):
    day: datetime
    count: int


class NewRecordResponse(IDModelMixin, CreatedAtMixin):
    pass


class UpdatedRecordResponse(IDModelMixin, UpdatedAtMixin):
    pass


class TimestampsMixin(CreatedAtMixin, UpdatedAtMixin):
    pass


Count = CreatedCount


class BooleanResponse(BaseModel):
    value: bool


class StringResponse(BaseModel):
    value: str


class GenericError(BaseModel):
    message: str


NotFound = GenericError
InvalidToken = GenericError
NotPermitted = GenericError


class FileMismatchError(GenericError):
    message: str = "The file is not in the expected file format."


def decode_json(cls, v):
    if not isinstance(v, str):
        try:
            return json.dumps(v)
        except Exception as err:
            raise ValueError(f"Could not parse value into valid JSON: {err}")

    return v
