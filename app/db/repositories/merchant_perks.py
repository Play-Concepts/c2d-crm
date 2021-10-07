import uuid
from typing import List, Optional

from app.models.core import IDModelMixin
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

LIKE_MERCHANT_PERK_SQL = """
    INSERT INTO merchant_perk_favourites(merchant_perk_id, pda_url)
    VALUES(:merchant_perk_id, :pda_url)
    ON CONFLICT(merchant_perk_id, pda_url)
    DO UPDATE SET updated_at = now()
    RETURNING id;
"""

UNLIKE_MERCHANT_PERK_SQL = """
    DELETE FROM merchant_perk_favourites WHERE merchant_perk_id=:merchant_perk_id
    AND pda_url=:pda_url
    RETURNING id;
"""

GET_CUSTOMER_FAVOURITED_PERKS_SQL = """
    SELECT merchant_perks.id, merchant_perks.title, merchant_perks.details, merchant_perks.start_date,
    merchant_perks.end_date, merchant_perks.perk_url, merchant_perks.logo_url, merchant_perks.perk_image_url,
    true AS favourited FROM merchant_perks WHERE id IN
    (SELECT merchant_perk_id FROM merchant_perk_favourites WHERE pda_url = :pda_url);
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

    async def like_merchant_perk(
        self, *, merchant_perk_id: uuid.UUID, pda_url: str
    ) -> IDModelMixin:
        query_values = {"merchant_perk_id": merchant_perk_id, "pda_url": pda_url}
        perk = await self.db.fetch_one(
            query=LIKE_MERCHANT_PERK_SQL, values=query_values
        )
        return IDModelMixin(**perk)

    async def unlike_merchant_perk(
        self, *, merchant_perk_id: uuid.UUID, pda_url: str
    ) -> Optional[IDModelMixin]:
        query_values = {"merchant_perk_id": merchant_perk_id, "pda_url": pda_url}
        perk = await self.db.fetch_one(
            query=UNLIKE_MERCHANT_PERK_SQL, values=query_values
        )
        return None if perk is None else IDModelMixin(**perk)

    async def get_customer_favourited_perks(
        self, *, pda_url: str
    ) -> List[MerchantPerkCustomerView]:
        query_values = {"pda_url": pda_url}
        perks = await self.db.fetch_all(
            query=GET_CUSTOMER_FAVOURITED_PERKS_SQL, values=query_values
        )
        return [MerchantPerkCustomerView(**perk) for perk in perks]
