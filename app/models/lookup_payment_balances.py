from app.models.core import CoreModel, IDModelMixin, TimestampsMixin


class LookupPaymentBalanceBase(CoreModel):
    currency: str
    amount: int
    creditable_balance: int


class LookupPaymentBalanceDBModel(
    IDModelMixin, LookupPaymentBalanceBase, TimestampsMixin
):
    pass


LookupPaymentBalance = LookupPaymentBalanceDBModel
