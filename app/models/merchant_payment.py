import uuid

from app.models.core import CoreModel, IDModelMixin, TimestampsMixin


class MerchantPaymentBase(CoreModel):
    merchant_id: uuid.UUID
    currency: str
    amount: int
    payment_identifier: str
    status: str


class MerchantPaymentDBModel(IDModelMixin, MerchantPaymentBase, TimestampsMixin):
    pass


class MerchantPayment(IDModelMixin, MerchantPaymentBase):
    pass


MerchantPaymentNew = MerchantPaymentBase


class MerchantPaymentUpdate(IDModelMixin):
    status: str
