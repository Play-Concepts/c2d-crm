import uuid
from typing import Optional

from pydantic.class_validators import validator
from pydantic.types import Json

from app.models.core import CoreModel, IDModelMixin, decode_json


class DataPassSourceBase(CoreModel):
    name: str
    description: str
    logo_url: str
    data_table: str
    search_sql: str
    data_descriptors: Json

    @validator("data_descriptors", pre=True)
    def decode_json(cls, v):
        return decode_json(cls, v)


class DataPassSourceDB(IDModelMixin, DataPassSourceBase):
    pass


class DataPassSourceNew(DataPassSourceBase):
    user_id: uuid.UUID


DataPassSourceRequest = DataPassSourceBase


class DataPassSourceDescriptor(CoreModel):
    data_table: str
    search_sql: Optional[str]
    data_descriptors: Optional[Json]
    user_id: Optional[uuid.UUID]
