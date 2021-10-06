import uuid
from datetime import datetime
from typing import Optional

from app.models.core import CoreModel, IDModelMixin, TimestampsMixin


class MerchantPerkBase(CoreModel):
    title: str
    details: str
    start_date: datetime
    end_date: Optional[datetime]
    perk_url: str
    logo_url: Optional[str]
    perk_image_url: Optional[str]


class MerchantPerkCustomerView(IDModelMixin, MerchantPerkBase):
    favourited: bool


class MerchantPerkDBModel(IDModelMixin, MerchantPerkBase, TimestampsMixin):
    merchant_id: Optional[uuid.UUID]
