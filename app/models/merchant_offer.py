import uuid
from datetime import datetime
from typing import List, Optional

from app.models.core import (CoreModel, IDModelMixin, NotPermitted,
                             TimestampsMixin)


class ImagesMixIn(CoreModel):
    logo_url: Optional[str]
    offer_image_url: Optional[str]


class DataPassesMixin(CoreModel):
    data_passes: Optional[List[uuid.UUID]]


class MerchantOfferBase(CoreModel):
    title: str
    details: str
    start_date: datetime
    end_date: Optional[datetime]
    offer_url: str


class MerchantOfferCustomerView(IDModelMixin, MerchantOfferBase, ImagesMixIn):
    pass


class MerchantOfferDBModel(
    IDModelMixin, MerchantOfferBase, ImagesMixIn, TimestampsMixin
):
    merchant_id: Optional[uuid.UUID]


class MerchantOfferNewRequest(MerchantOfferBase, DataPassesMixin):
    pass


class MerchantOfferNew(MerchantOfferBase):
    merchant_id: Optional[uuid.UUID]

    def before_save(self):
        self.start_date = self.start_date.replace(tzinfo=None)
        if self.end_date is not None:
            self.end_date = self.end_date.replace(tzinfo=None)


class MerchantOfferUpdateRequest(IDModelMixin, MerchantOfferBase, DataPassesMixin):
    status: str


class MerchantOfferUpdate(IDModelMixin, MerchantOfferBase):
    status: str

    def before_save(self):
        self.start_date = self.start_date.replace(tzinfo=None)
        if self.end_date is not None:
            self.end_date = self.end_date.replace(tzinfo=None)


class MerchantOfferMerchantView(
    IDModelMixin, MerchantOfferBase, DataPassesMixin, ImagesMixIn
):
    status: str


class ForbiddenMerchantOfferAccess(NotPermitted):
    message: str = "You do not have permission to access this Merchant Offer."
