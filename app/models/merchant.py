#     op.create_table(
#         "merchants",
#         sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
#         sa.Column("first_name", sa.VARCHAR(128), nullable=False),
#         sa.Column("last_name", sa.VARCHAR(128), nullable=False),
#         sa.Column("company_name", sa.VARCHAR(128), nullable=False),
#         sa.Column("trade_name", sa.VARCHAR(128), nullable=True),
#         sa.Column("address", sa.VARCHAR(4096), nullable=True),
#         sa.Column("email", sa.VARCHAR(255), nullable=False, unique=True),
#         sa.Column("phone_number", sa.VARCHAR(47), nullable=True),
#         sa.Column("offer", JSON, nullable=True),
#         sa.Column("welcome_email_sent", sa.BOOLEAN, nullable=False, default=False)
#     )
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


class MerchantView(IDModelMixin):
    pass


class MerchantEmailView(IDModelMixin, MerchantBasicModel):
    pass


class MerchantEmailSentView(IDModelMixin):
    welcome_email_sent: datetime
