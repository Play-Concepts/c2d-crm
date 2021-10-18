import json
import uuid
from typing import List, Optional

from app.apis.utils.random import random_string
from app.db.repositories.base import BaseRepository
from app.models.core import IDModelMixin
from app.models.merchant import (MerchantEmailSentView, MerchantEmailView,
                                 MerchantNew)

NEW_MERCHANT_SQL = """
    INSERT INTO merchants(first_name, last_name, company_name, trade_name, address, email, phone_number,
    offer, logo_url, password_change_token, terms_agreed)
    VALUES(:first_name, :last_name, :company_name, :trade_name, :address, :email, :phone_number,
    :offer, :logo_url, :password_change_token, :terms_agreed)
    ON CONFLICT(email) DO NOTHING
    RETURNING id;
"""

WELCOME_EMAIL_LIST_SQL = """
    SELECT id, first_name, last_name, email, company_name, address, phone_number,
     password_change_token FROM merchants WHERE welcome_email_sent is null;
"""

UPDATE_WELCOME_EMAIL_SENT_SQL = """
    UPDATE merchants SET welcome_email_sent=now(), updated_at=now() WHERE id=:id
    RETURNING id, welcome_email_sent;
"""

GET_MERCHANT_BY_EMAIL_SQL = """
    SELECT id, first_name, email, password_change_token FROM merchants WHERE email=:email;
"""


class MerchantsRepository(BaseRepository):
    async def create_merchant(
        self, *, new_merchant: MerchantNew
    ) -> Optional[IDModelMixin]:
        query_values = new_merchant.dict()
        query_values["offer"] = json.dumps(new_merchant.offer)
        query_values["password_change_token"] = random_string(40)
        created_merchant = await self.db.fetch_one(
            query=NEW_MERCHANT_SQL, values=query_values
        )
        return None if created_merchant is None else IDModelMixin(**created_merchant)

    async def get_merchants_email_list(self) -> List[MerchantEmailView]:
        merchants = await self.db.fetch_all(query=WELCOME_EMAIL_LIST_SQL)
        return [MerchantEmailView(**merchant) for merchant in merchants]

    async def update_welcome_email_sent(
        self, *, merchant_id: uuid.UUID
    ) -> MerchantEmailSentView:
        updated_merchant = await self.db.fetch_one(
            query=UPDATE_WELCOME_EMAIL_SENT_SQL, values={"id": merchant_id}
        )
        return MerchantEmailSentView(**updated_merchant)

    async def get_merchant_by_email(self, *, email: str) -> MerchantEmailView:
        merchant = await self.db.fetch_one(
            query=GET_MERCHANT_BY_EMAIL_SQL, values={"email": email}
        )
        return None if merchant is None else MerchantEmailView(**merchant)
