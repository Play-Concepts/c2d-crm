import json
import uuid
from typing import Optional

from app.db.repositories.base import BaseRepository
from app.models.merchant import MerchantNew, MerchantView


NEW_MERCHANT_SQL = """
    INSERT INTO merchants(id, first_name, last_name, company_name, trade_name, address, email, phone_number, offer, logo_url, welcome_email_sent) 
    VALUES(:id, :first_name, :last_name, :company_name, :trade_name, :address, :email, :phone_number, :offer, :logo_url, :welcome_email_sent) 
    ON CONFLICT(email) DO NOTHING 
    RETURNING id;
"""


class MerchantsRepository(BaseRepository):
    async def create_merchant(self, *, new_merchant: MerchantNew) -> Optional[MerchantView]:
        new_merchant.id = uuid.uuid4()
        query_values = new_merchant.dict()
        query_values['offer'] = json.dumps(new_merchant.offer)
        created_merchant = await self.db.fetch_one(query=NEW_MERCHANT_SQL, values=query_values)
        return None if created_merchant is None else MerchantView(**created_merchant)
