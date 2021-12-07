import uuid
from typing import Optional

from app.models.core import NewRecordResponse
from app.models.merchant_offer_data_pass import MerchantOfferDataPassNew

from .base import BaseRepository

CREATE_MERCHANT_OFFER_DATA_PASS_SQL = """
    INSERT INTO merchant_offers_data_passes(merchant_offer_id, data_pass_id)
    VALUES(:merchant_offer_id, :data_pass_id)
    ON CONFLICT(merchant_offer_id, data_pass_id)
    DO UPDATE SET updated_at = now(), status='active'
    RETURNING id, created_at;
"""

GET_MERCHANT_OFFER_DATA_PASSES_SQL = """
    SELECT id, merchant_offer_id, data_pass_id, valid_until, status FROM merchant_offers_data_passes
    WHERE merchant_offer_id=:merchant_offer_id;
"""

DISABLE_MERCHANT_OFFER_DATA_PASSES_SQL = """
    UPDATE merchant_offers_data_passes SET status='inactive', updated_at = now()
    WHERE merchant_offer_id=:merchant_offer_id;
"""


class MerchantOffersDataPassesRepository(BaseRepository):
    async def create_merchant_offer_data_pass(
        self, *, merchant_offer_data_pass_new: MerchantOfferDataPassNew
    ) -> Optional[NewRecordResponse]:
        merchant_offer_data_pass = await self.db.fetch_one(
            query=CREATE_MERCHANT_OFFER_DATA_PASS_SQL,
            values=merchant_offer_data_pass_new.dict(),
        )
        return (
            None
            if merchant_offer_data_pass is None
            else NewRecordResponse(**merchant_offer_data_pass)
        )

    async def disable_all_merchant_offer_data_passes(
        self,
        *,
        merchant_offer_id: uuid.UUID,
    ):
        return await self.db.fetch_one(
            query=DISABLE_MERCHANT_OFFER_DATA_PASSES_SQL,
            values={
                "merchant_offer_id": merchant_offer_id,
            },
        )
