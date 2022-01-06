import uuid
from datetime import datetime
from enum import Enum
from hashlib import md5
from typing import List, Optional

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
    data: Json
    data_hash: Optional[str]

    def dot_to_key(self, dot) -> str:
        keys = ['["{}"]'.format(item) for item in dot.split(".")]
        return "".join(keys)

    def generate_hash(self, *, keys: List[str]):
        hash_data = ""
        for key in keys:
            hash_data += str(eval("self.data" + self.dot_to_key(key)))

        hash_target = hash_data.replace(" ", "").lower().encode("utf-8")
        self.data_hash = md5(hash_target).hexdigest()

    before_save = generate_hash


class CustomerUpdate(CustomerBase):
    status: Optional[StatusType]


class CustomerDBModel(IDModelMixin, CustomerBase):
    data: Json
    status: StatusType
    pda_url: Optional[str]


class CustomerView(IDModelMixin, CustomerBase):
    data: Optional[Json]
    total_count: Optional[int]


class CustomerSearch(CoreModel):
    last_name: Optional[str] = ""
    address: Optional[str] = ""
    email: Optional[str] = ""
    data_pass_id: uuid.UUID


class CustomerClaim(IDModelMixin):
    pass


class CustomerClaimResponse(IDModelMixin, CustomerBase):
    data: Json
    status: Optional[StatusType]
    pda_url: Optional[str]
    claimed_timestamp: Optional[datetime]

    data_table: Optional[str]
