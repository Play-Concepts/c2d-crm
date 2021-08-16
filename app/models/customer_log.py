from datetime import datetime
from typing import Optional

from app.models.core import CoreModel, IDModelMixin


class CustomerLogBase(CoreModel):
    pda_url: Optional[str]
    event: Optional[str]


class CustomerLogNew(CustomerLogBase):
    pass


class CustomerLog(IDModelMixin, CustomerLogBase):
    created_at: datetime


class CustomerLogDBModel(IDModelMixin, CustomerLogBase):
    created_at: Optional[datetime]
