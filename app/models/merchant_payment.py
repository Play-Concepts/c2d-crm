import uuid

from app.models.core import CoreModel, IDModelMixin, TimestampsMixin


class MerchantPaymentBase(CoreModel):
    user_id: uuid.UUID
    amount: int
    payment_identifier: str
    status: str


class MerchantPaymentDBModel(IDModelMixin, MerchantPaymentBase, TimestampsMixin):
    pass


MerchantPayment = MerchantPaymentDBModel
