import uuid
from datetime import datetime
from typing import Optional

from app.models.core import CoreModel, IDModelMixin, TimestampsMixin


class MerchantOfferBase(CoreModel):
    title: str
    details: str
    start_date: datetime
    end_date: Optional[datetime]
    offer_url: str
    logo_url: Optional[str]
    offer_image_url: Optional[str]


class MerchantOfferCustomerView(IDModelMixin, MerchantOfferBase):
    pass


class MerchantOfferDBModel(IDModelMixin, MerchantOfferBase, TimestampsMixin):
    merchant_id: Optional[uuid.UUID]


class MerchantOfferNew(MerchantOfferBase):
    merchant_id: uuid.UUID


class MerchantOfferMerchantView(IDModelMixin, MerchantOfferBase):
    pass
