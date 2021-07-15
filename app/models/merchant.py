from typing import Optional

from pydantic.class_validators import validator

from app.models.core import IDModelMixin, CoreModel, decode_json
from pydantic.types import Json
from datetime import datetime


class MerchantBasicModel(CoreModel):
    first_name: str
    email: str


class MerchantBase(MerchantBasicModel):
    last_name: str
    company_name: str
    trade_name: Optional[str]
    address: Optional[str]
    phone_number: Optional[str]
    offer: Optional[Json]
    logo_url: Optional[str]

    @validator('offer', pre=True)
    def decode_json(cls, v):
        return decode_json(cls, v)


class MerchantNew(IDModelMixin, MerchantBase):
    pass


class MerchantDBModel(IDModelMixin, MerchantBase):
    welcome_email_sent: Optional[datetime]
    password_change_token: Optional[str]


class MerchantView(IDModelMixin):
    pass


class MerchantEmailView(IDModelMixin, MerchantBasicModel):
    password_change_token: str


class MerchantEmailSentView(IDModelMixin):
    welcome_email_sent: datetime
