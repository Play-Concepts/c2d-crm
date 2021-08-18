import uuid
from datetime import datetime
from typing import Optional

from app.models.core import CoreModel, IDModelMixin


class ScanTransactionBase(CoreModel):
    customer_id: Optional[uuid.UUID]
    user_id: Optional[uuid.UUID]


class ScanTransactionNew(ScanTransactionBase):
    pass


class ScanTransactionDBModel(IDModelMixin, ScanTransactionBase):
    created_at: datetime


class ScanTransactionBasicView(IDModelMixin):
    pass


ScanTransactionView = ScanTransactionDBModel


class ScanRequest(CoreModel):
    barcode: str


class ScanResult(CoreModel):
    verified: bool


class ScanTransactionCount(CoreModel):
    valid: int
    total: int
    fails: Optional[int]
    from_date: datetime
    to_date: datetime

    def compute(self):
        self.fails = self.total - self.valid
        return self


class ScanTransactionCounts(CoreModel):
    interval_1: Optional[ScanTransactionCount]
    interval_2: Optional[ScanTransactionCount]
    interval_3: Optional[ScanTransactionCount]
