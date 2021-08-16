from datetime import datetime
from typing import Optional

from pydantic.class_validators import validator
from pydantic.types import Json

from app.models.core import CoreModel, IDModelMixin, decode_json


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
    terms_agreed: bool

    @validator("offer", pre=True)
    def decode_json(cls, v):
        return decode_json(cls, v)


class MerchantNew(MerchantBase):
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
