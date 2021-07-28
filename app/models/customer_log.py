import uuid
from datetime import datetime
from typing import Optional

from app.models.core import CoreModel, IDModelMixin


class CustomerLogBase(CoreModel):
    pda_url: Optional[str]
    event: Optional[str]
    created_at: Optional[datetime]


class CustomerLogNew(IDModelMixin, CustomerLogBase):
    def new(self):
        self.id = uuid.uuid4()
        self.created_at = datetime.now()
        return self


class CustomerLogDBModel(IDModelMixin, CustomerLogBase):
    pass
