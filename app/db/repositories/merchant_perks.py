import uuid
from typing import List, Optional

from app.models.core import IDModelMixin
from app.models.merchant_perk import (MerchantPerkCustomerView,
                                      MerchantPerkDBModel,
                                      MerchantPerkMerchantView,
                                      MerchantPerkNew)

from .base import BaseRepository

GET_CUSTOMER_PERKS_SQL = """
    SELECT merchant_perks.id, merchant_perks.title, merchant_perks.details, merchant_perks.start_date,
    merchant_perks.end_date, merchant_perks.perk_url, merchant_perks.logo_url, merchant_perks.perk_image_url
    FROM merchant_perks JOIN merchant_perks_data_passes
    ON (merchant_perks_data_passes.merchant_perk_id=merchant_perks.id)
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
    merchant_perks.end_date, merchant_perks.perk_url, merchant_perks.logo_url, merchant_perks.perk_image_url
    FROM merchant_perks WHERE id IN
    (SELECT merchant_perk_id FROM merchant_perk_favourites WHERE pda_url = :pda_url);
"""

GET_ALL_CUSTOMER_PERKS_SQL = """
    SELECT merchant_perks.id, merchant_perks.title, merchant_perks.details, merchant_perks.start_date,
    merchant_perks.end_date, merchant_perks.perk_url, merchant_perks.logo_url, merchant_perks.perk_image_url
    FROM merchant_perks;
"""

GET_MERCHANT_PERKS_SQL = """
    SELECT merchant_perks.id, merchant_perks.title, merchant_perks.details, merchant_perks.start_date,
    merchant_perks.end_date, merchant_perks.perk_url, merchant_perks.logo_url, merchant_perks.perk_image_url
    FROM merchant_perks WHERE merchant_id IN (SELECT id FROM merchants WHERE email=:email);
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

    async def get_all_customer_perks(self) -> List[MerchantPerkCustomerView]:
        perks = await self.db.fetch_all(query=GET_ALL_CUSTOMER_PERKS_SQL)
        return [MerchantPerkCustomerView(**perk) for perk in perks]

    async def get_merchant_perks(
        self,
        *,
        email: str,
    ) -> List[MerchantPerkMerchantView]:
        query_values = {"email": email}
        perks = await self.db.fetch_all(
            query=GET_MERCHANT_PERKS_SQL, values=query_values
        )
        return [MerchantPerkMerchantView(**perk) for perk in perks]

    # TODO: TRANSIENT - not currently used in application, only in test suite
    async def get_merchant_perk_(
        self, *, merchant_perk_id: uuid.UUID
    ) -> List[MerchantPerkDBModel]:
        sql = """
            SELECT * FROM merchant_perks WHERE id = :merchant_perk_id;
        """
        query_values = {"merchant_perk_id": merchant_perk_id}
        perks = await self.db.fetch_all(query=sql, values=query_values)
        return [MerchantPerkDBModel(**perk) for perk in perks]

    # TODO: TRANSIENT - not currently used in application, only in test suite
    async def create_merchant_perk_(
        self, *, merchant_perk_new: MerchantPerkNew
    ) -> IDModelMixin:
        sql = """
            INSERT INTO merchant_perks(merchant_id, title, details, start_date,
            perk_url, logo_url, perk_image_url)
            VALUES(:merchant_id, :title, :details, :start_date,
            :perk_url, :logo_url, :perk_image_url) RETURNING id;
        """
        perks = await self.db.fetch_all(query=sql, values=merchant_perk_new.dict())
        return [MerchantPerkDBModel(**perk) for perk in perks]
