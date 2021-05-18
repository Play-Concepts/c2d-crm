from typing import Optional
from pydantic import Json
from enum import Enum
from app.models.core import IDModelMixin, CoreModel


class StatusType(str, Enum):
    new = 'new'
    claimed = 'claimed'


class CustomerBase(CoreModel):
    data: Optional[Json]
    status: Optional[StatusType] = 'new'
    pda_url: Optional[str]


class CustomerNew(CustomerBase):
    data: Json


class CustomerUpdate(CustomerBase):
    status: Optional[StatusType]


class CustomerDBModel(IDModelMixin, CustomerBase):
    data: Json
    status: StatusType
    pda_url: Optional[str]


class CustomerView(IDModelMixin, CustomerBase):
    pass
