import uuid

from app.models.core import CoreModel, IDModelMixin, TimestampsMixin


class MerchantBalanceBase(CoreModel):
    user_id: uuid.UUID
    amount: int
    balance_type: str


class MerchantBalanceDBModel(IDModelMixin, MerchantBalanceBase, TimestampsMixin):
    pass


MerchantBalance = MerchantBalanceDBModel
