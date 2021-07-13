import json
import uuid
from typing import Optional, List

from app.db.repositories.base import BaseRepository
from app.models.merchant import MerchantNew, MerchantView, MerchantEmailView, MerchantEmailSentView


NEW_MERCHANT_SQL = """
    INSERT INTO merchants(id, first_name, last_name, company_name, trade_name, address, email, phone_number, offer, logo_url, welcome_email_sent) 
    VALUES(:id, :first_name, :last_name, :company_name, :trade_name, :address, :email, :phone_number, :offer, :logo_url, :welcome_email_sent) 
    ON CONFLICT(email) DO NOTHING 
    RETURNING id;
"""

WELCOME_EMAIL_LIST_SQL = """
    SELECT id, first_name, email FROM merchants WHERE welcome_email_sent is null;
"""

UPDATE_WELCOME_EMAIL_SENT_SQL = """
    UPDATE merchants SET welcome_email_sent=now() WHERE id=:id 
    RETURNING id, welcome_email_sent;
"""


class MerchantsRepository(BaseRepository):
    async def create_merchant(self, *, new_merchant: MerchantNew) -> Optional[MerchantView]:
        new_merchant.id = uuid.uuid4()
        query_values = new_merchant.dict()
        query_values['offer'] = json.dumps(new_merchant.offer)
        created_merchant = await self.db.fetch_one(query=NEW_MERCHANT_SQL, values=query_values)
        return None if created_merchant is None else MerchantView(**created_merchant)

    async def get_merchants_email_list(self) -> List[MerchantEmailView]:
        merchants = await self.db.fetch_all(query=WELCOME_EMAIL_LIST_SQL)
        return [MerchantEmailView(**merchant) for merchant in merchants]

    async def update_welcome_email_sent(self, *, merchant_id: uuid.UUID) -> MerchantEmailSentView:
        updated_merchant = await self.db.fetch_one(query=UPDATE_WELCOME_EMAIL_SENT_SQL, values={"id": merchant_id})
        return MerchantEmailSentView(**updated_merchant)
