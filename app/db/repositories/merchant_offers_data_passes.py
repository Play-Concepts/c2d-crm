import uuid
from typing import List, Optional

from app.models.core import NewRecordResponse, UpdatedRecordResponse
from app.models.merchant_offer_data_pass import (MerchantOfferDataPass,
                                                 MerchantOfferDataPassNew)

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
    WHERE merchant_offer_id=:merchant_offer_id
    RETURNING id, updated_at;
"""

GET_MERCHANT_OFFERS_DATA_PASSES_REQUIRING_PAYMENTS_SQL = """
    SELECT id, merchant_offer_id, data_pass_id, valid_until, status FROM merchant_offers_data_passes
    WHERE merchant_offer_id=:merchant_offer_id AND valid_until IS NULL AND status = 'active';
"""

SET_VALID_TILL_END_OF_MONTH = """
    UPDATE merchant_offers_data_passes SET updated_at = now(),
    valid_until = (date_trunc('month', now()::date + INTERVAL '1 month') - INTERVAL '1 second')
    WHERE merchant_offer_id=:merchant_offer_id
    RETURNING id, updated_at;
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
    ) -> List[UpdatedRecordResponse]:
        updated_records = await self.db.fetch_all(
            query=DISABLE_MERCHANT_OFFER_DATA_PASSES_SQL,
            values={
                "merchant_offer_id": merchant_offer_id,
            },
        )
        return [
            UpdatedRecordResponse(**updated_records)
            for updated_records in updated_records
        ]

    async def get_merchant_offers_data_passes_requiring_payments(
        self, *, merchant_offer_id: uuid.UUID
    ) -> List[MerchantOfferDataPass]:
        merchant_offers_data_passes = await self.db.fetch_all(
            query=GET_MERCHANT_OFFERS_DATA_PASSES_REQUIRING_PAYMENTS_SQL,
            values={"merchant_offer_id": merchant_offer_id},
        )
        return [MerchantOfferDataPass(**offer) for offer in merchant_offers_data_passes]

    async def set_merchant_offer_data_pass_validity(
        self, *, merchant_offer_id: uuid.UUID
    ) -> Optional[UpdatedRecordResponse]:
        merchant_offer_data_pass = await self.db.fetch_one(
            query=SET_VALID_TILL_END_OF_MONTH,
            values={"merchant_offer_id": merchant_offer_id},
        )
        return (
            None
            if merchant_offer_data_pass is None
            else UpdatedRecordResponse(**merchant_offer_data_pass)
        )
