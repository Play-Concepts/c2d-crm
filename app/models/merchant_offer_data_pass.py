import uuid
from datetime import datetime
from typing import Optional

from app.models.core import CoreModel, IDModelMixin, TimestampsMixin


class MerchantOfferDataPassBase(CoreModel):
    merchant_offer_id: uuid.UUID
    data_pass_id: uuid.UUID


class MerchantOfferDataPassStatusMixin(CoreModel):
    valid_until: Optional[datetime]
    status: str


class MerchantOfferDataPass(
    IDModelMixin, MerchantOfferDataPassBase, MerchantOfferDataPassStatusMixin
):
    pass


class MerchantOfferDataPassDBModel(
    IDModelMixin,
    MerchantOfferDataPassBase,
    MerchantOfferDataPassStatusMixin,
    TimestampsMixin,
):
    pass


MerchantOfferDataPassNew = MerchantOfferDataPassBase


class MerchantOfferDataPassUpdateRequest(IDModelMixin):
    valid_until: Optional[datetime]
    status: str

    def before_save(self):
        if self.valid_until is not None:
            self.valid_until = self.valid_until.replace(tzinfo=None)
