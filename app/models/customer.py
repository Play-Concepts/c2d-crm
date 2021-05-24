from typing import Optional
from enum import Enum

from pydantic.class_validators import validator
from pydantic.main import BaseModel

from app.models.core import IDModelMixin, CoreModel
from pydantic.types import Json
import json


class StatusType(str, Enum):
    new = 'new'
    claimed = 'claimed'


class CustomerBase(CoreModel):
    data: Optional[Json]
    status: Optional[StatusType] = 'new'
    pda_url: Optional[str]

    @validator('data', pre=True)
    def decode_json(cls, v):
        if not isinstance(v, str):
            try:
                return json.dumps(v)
            except Exception as err:
                raise ValueError(f'Could not parse value into valid JSON: {err}')

        return v


class CustomerNew(CustomerBase):
    data: Json


class CustomerUpdate(CustomerBase):
    status: Optional[StatusType]


class CustomerDBModel(IDModelMixin, CustomerBase):
    data: Json
    status: StatusType
    pda_url: Optional[str]


class CustomerView(IDModelMixin, CustomerBase):
    data: Json
    total_count: Optional[int]


class CustomerBasicView(IDModelMixin):
    pass


class CustomerSearch(BaseModel):
    last_name: Optional[str] = ''
    house_number: Optional[str] = ''
    email: Optional[str] = ''


class CustomerClaim(IDModelMixin):
    pass


class CustomerClaimResponse(IDModelMixin, CustomerBase):
    data: Json
    status: StatusType
    pda_url: str
