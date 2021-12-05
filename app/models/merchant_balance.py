import uuid
from enum import Enum

from app.models.core import CoreModel, IDModelMixin, TimestampsMixin


class MerchantBalanceBase(CoreModel):
    merchant_id: uuid.UUID
    amount: int
    balance_type: str


class MerchantBalanceDBModel(IDModelMixin, MerchantBalanceBase, TimestampsMixin):
    pass


MerchantBalance = MerchantBalanceDBModel
MerchantBalanceNew = MerchantBalanceBase


class MerchantBalanceAmount(CoreModel):
    amount: int


class BalanceType(str, Enum):
    credit = "credit"
    debit = "debit"
