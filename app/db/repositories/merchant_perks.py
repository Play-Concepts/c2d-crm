import uuid
from typing import List, Optional

from app.models.merchant_perk import MerchantPerkCustomerView

from .base import BaseRepository


GET_CUSTOMER_PERKS_SQL = """
    SELECT merchant_perks.id, merchant_perks.title, merchant_perks.details, merchant_perks.start_date,
    merchant_perks.end_date, merchant_perks.perk_url, merchant_perks.logo_url, merchant_perks.perk_image_url,
    CASE WHEN mpf.id IS null THEN false ELSE true END AS favourited FROM merchant_perks
    JOIN merchant_perks_data_passes ON (merchant_perks_data_passes.merchant_perk_id=merchant_perks.id)
    LEFT JOIN (SELECT * FROM merchant_perk_favourites WHERE pda_url=:pda_url) mpf
    ON (mpf.merchant_perk_id=merchant_perks_data_passes.merchant_perk_id)
    WHERE merchant_perks_data_passes.data_pass_id=:data_pass_id;
"""

class MerchantPerksRepository(BaseRepository):
    async def get_customer_perks(
        self, *, data_pass_id: uuid.UUID, pda_url: str
    ) -> List[MerchantPerkCustomerView]:
        query_values = {"data_pass_id": data_pass_id, "pda_url": pda_url}
        perks = await self.db.fetch_all(
            query=GET_CUSTOMER_PERKS_SQL, values=query_values
        )
        return [MerchantPerkCustomerView(**perk) for perk in perks]
