from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.models.core import CoreModel, IDModelMixin, NotPermitted


class StatusType(str, Enum):
    active = "active"
    inactive = "inactive"


class DataPassSourceVerifier(CoreModel):
    source_name: str
    source_description: str
    source_logo_url: str
    verifier_name: str
    verifier_description: str
    verifier_logo_url: str


class DataPassBase(CoreModel):
    name: str
    title: str
    description_for_merchants: Optional[str]
    description_for_customers: Optional[str]
    offers_url_for_merchants: Optional[str]
    offers_url_for_customers: Optional[str]
    details_url: Optional[str]
    expiry_days: Optional[int]
    expiry_date: Optional[datetime]


class DataPassBasicView(IDModelMixin):
    name: str


class DataPassCustomerView(IDModelMixin, DataPassBase, DataPassSourceVerifier):
    activation_status: Optional[StatusType]
    active_label_1: Optional[str] = "Confirmed"
    active_label_2: Optional[str] = ""
    inactive_label_1: Optional[str] = "Not Active"
    inactive_label_2: Optional[str] = ""


class DataPassMerchantView(IDModelMixin, DataPassBase, DataPassSourceVerifier):
    currency_code: str
    price: float
    status: Optional[StatusType]


class InvalidDataPass(BaseModel):
    verified: bool = False
    expired: bool = False
    message: str = "Data Pass is not found or may have expired."


class ForbiddenDataPass(NotPermitted):
    message: str = "You do not have permission to access this Data Pass."
