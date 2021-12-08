import uuid
from enum import Enum
from typing import Optional

from app.models.core import CoreModel, IDModelMixin, TimestampsMixin


class MerchantBalanceBase(CoreModel):
    merchant_id: uuid.UUID
    amount: int
    balance_type: str
    transaction_identifier: Optional[uuid.UUID]


class MerchantBalanceDBModel(IDModelMixin, MerchantBalanceBase, TimestampsMixin):
    pass


MerchantBalance = MerchantBalanceDBModel
MerchantBalanceNew = MerchantBalanceBase


class MerchantBalanceAmount(CoreModel):
    amount: int


class BalanceType(str, Enum):
    credit = "credit"
    debit = "debit"
