import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic.class_validators import validator
from pydantic.types import Json

from app.models.core import CoreModel, IDModelMixin, decode_json


class StatusType(str, Enum):
    new = "new"
    claimed = "claimed"


class CustomerBase(CoreModel):
    data: Optional[Json]
    status: Optional[StatusType] = "new"
    pda_url: Optional[str]

    @validator("data", pre=True)
    def decode_json(cls, v):
        return decode_json(cls, v)


class CustomerNew(CustomerBase):
    data_pass_id: uuid.UUID
    data: Json


class CustomerUpdate(CustomerBase):
    status: Optional[StatusType]


class CustomerDBModel(IDModelMixin, CustomerBase):
    data: Json
    status: StatusType
    pda_url: Optional[str]


class CustomerView(IDModelMixin, CustomerBase):
    data: Optional[Json]
    total_count: Optional[int]


class CustomerBasicView(IDModelMixin):
    claimed_timestamp: Optional[datetime]


class CustomerSearch(CoreModel):
    last_name: Optional[str] = ""
    address: Optional[str] = ""
    email: Optional[str] = ""
    data_pass_id: uuid.UUID


class CustomerClaim(IDModelMixin):
    pass


class CustomerClaimResponse(IDModelMixin, CustomerBase):
    data: Json
    status: StatusType
    pda_url: str
    claimed_timestamp: datetime
    data_pass_id: uuid.UUID
