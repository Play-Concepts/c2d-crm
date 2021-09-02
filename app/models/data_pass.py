from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.models.core import CoreModel, IDModelMixin


class StatusType(str, Enum):
    active = "active"
    inactive = "inactive"


class DataPassSource(CoreModel):
    source_name: str
    source_description: str
    source_logo_url: str


class DataPassVerifier(CoreModel):
    verifier_name: str
    verifier_description: str
    verifier_logo_url: str


class DataPassBase(CoreModel):
    name: str
    title: str
    description_for_merchants: Optional[str]
    description_for_customers: Optional[str]
    perks_url_for_merchants: Optional[str]
    perks_url_for_customers: Optional[str]
    details_url: Optional[str]
    expiry_date: Optional[datetime]


class DataPassCustomerView(
    IDModelMixin, DataPassBase, DataPassSource, DataPassVerifier
):
    activation_status: Optional[StatusType]
    active_label_1: Optional[str] = "Confirmed"
    active_label_2: Optional[str] = ""
    inactive_label_1: Optional[str] = "Not Active"
    inactive_label_2: Optional[str] = ""


class DataPassMerchantView(
    IDModelMixin, DataPassBase, DataPassSource, DataPassVerifier
):
    currency_code: str
    price: float
    status: Optional[StatusType]


class InvalidDataPass(BaseModel):
    verified: bool = False
    message: str = "Data Pass is not found or may have expired."
