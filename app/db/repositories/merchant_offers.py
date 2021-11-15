import uuid
from typing import List, Optional

from app.models.core import (BooleanResponse, IDModelMixin, NewRecordResponse,
                             UpdatedRecordResponse)
from app.models.merchant_offer import (MerchantOfferCustomerView,
                                       MerchantOfferDBModel,
                                       MerchantOfferMerchantView,
                                       MerchantOfferNew,
                                       MerchantOfferUpdateRequest)

from .base import BaseRepository

GET_CUSTOMER_OFFERS_SQL = """
    SELECT merchant_offers.id, merchant_offers.title, merchant_offers.details, merchant_offers.start_date,
    merchant_offers.end_date, merchant_offers.offer_url, merchant_offers.logo_url, merchant_offers.offer_image_url
    FROM merchant_offers JOIN merchant_offers_data_passes
    ON (merchant_offers_data_passes.merchant_offer_id=merchant_offers.id)
    WHERE merchant_offers_data_passes.data_pass_id=:data_pass_id
    AND merchant_offers.status='active';
"""


CREATE_MERCHANT_OFFER_SQL = """
    INSERT INTO merchant_offers(merchant_id, title, details, start_date, end_date, offer_url)
    VALUES(:merchant_id, :title, :details, :start_date, :end_date, :offer_url)
    RETURNING id, created_at;
"""

IS_MERCHANT_OFFER_UPDATEABLE_SQL = """
    SELECT EXISTS(SELECT 1 FROM merchant_offers WHERE id=:id and merchant_id=:merchant_id) AS value;
"""

UPDATE_MERCHANT_OFFER_SQL = """
    UPDATE merchant_offers SET title=:title, details=:details, start_date=:start_date,
    end_date=:end_date, offer_url=:offer_url, status=:status, updated_at=now()
    WHERE id = :id
    RETURNING id, updated_at;
"""

UPDATE_MERCHANT_OFFER_STATUS_SQL = """
    UPDATE merchant_offers SET status=:status, updated_at=now() WHERE id = :id
    RETURNING id, updated_at;
"""

LIKE_MERCHANT_OFFER_SQL = """
    INSERT INTO merchant_offer_favourites(merchant_offer_id, pda_url)
    VALUES(:merchant_offer_id, :pda_url)
    ON CONFLICT(merchant_offer_id, pda_url)
    DO UPDATE SET updated_at = now()
    RETURNING id;
"""

UNLIKE_MERCHANT_OFFER_SQL = """
    DELETE FROM merchant_offer_favourites WHERE merchant_offer_id=:merchant_offer_id
    AND pda_url=:pda_url
    RETURNING id;
"""

GET_CUSTOMER_FAVOURITED_OFFERS_SQL = """
    SELECT merchant_offers.id, merchant_offers.title, merchant_offers.details, merchant_offers.start_date,
    merchant_offers.end_date, merchant_offers.offer_url, merchant_offers.logo_url, merchant_offers.offer_image_url
    FROM merchant_offers WHERE id IN
    (SELECT merchant_offer_id FROM merchant_offer_favourites WHERE pda_url = :pda_url);
"""

GET_ALL_CUSTOMER_OFFERS_SQL = """
    SELECT merchant_offers.id, merchant_offers.title, merchant_offers.details, merchant_offers.start_date,
    merchant_offers.end_date, merchant_offers.offer_url, merchant_offers.logo_url, merchant_offers.offer_image_url
    FROM merchant_offers WHERE merchant_offers.status='active';
"""

GET_MERCHANT_OFFERS_SQL = """
    SELECT merchant_offers.id, merchant_offers.title, merchant_offers.details, merchant_offers.start_date,
    merchant_offers.end_date, merchant_offers.offer_url, merchant_offers.logo_url, merchant_offers.offer_image_url,
    merchant_offers.status
    FROM merchant_offers WHERE merchant_id IN (SELECT id FROM merchants WHERE email=:email);
"""


class MerchantOffersRepository(BaseRepository):
    async def get_customer_offers(
        self, *, data_pass_id: uuid.UUID
    ) -> List[MerchantOfferCustomerView]:
        query_values = {"data_pass_id": data_pass_id}
        offers = await self.db.fetch_all(
            query=GET_CUSTOMER_OFFERS_SQL, values=query_values
        )
        return [MerchantOfferCustomerView(**offer) for offer in offers]

    async def like_merchant_offer(
        self, *, merchant_offer_id: uuid.UUID, pda_url: str
    ) -> IDModelMixin:
        query_values = {"merchant_offer_id": merchant_offer_id, "pda_url": pda_url}
        offer = await self.db.fetch_one(
            query=LIKE_MERCHANT_OFFER_SQL, values=query_values
        )
        return IDModelMixin(**offer)

    async def unlike_merchant_offer(
        self, *, merchant_offer_id: uuid.UUID, pda_url: str
    ) -> Optional[IDModelMixin]:
        query_values = {"merchant_offer_id": merchant_offer_id, "pda_url": pda_url}
        offer = await self.db.fetch_one(
            query=UNLIKE_MERCHANT_OFFER_SQL, values=query_values
        )
        return None if offer is None else IDModelMixin(**offer)

    async def get_customer_favourited_offers(
        self, *, pda_url: str
    ) -> List[MerchantOfferCustomerView]:
        query_values = {"pda_url": pda_url}
        offers = await self.db.fetch_all(
            query=GET_CUSTOMER_FAVOURITED_OFFERS_SQL, values=query_values
        )
        return [MerchantOfferCustomerView(**offer) for offer in offers]

    async def get_all_customer_offers(self) -> List[MerchantOfferCustomerView]:
        offers = await self.db.fetch_all(query=GET_ALL_CUSTOMER_OFFERS_SQL)
        return [MerchantOfferCustomerView(**offer) for offer in offers]

    async def get_merchant_offers(
        self,
        *,
        email: str,
    ) -> List[MerchantOfferMerchantView]:
        query_values = {"email": email}
        offers = await self.db.fetch_all(
            query=GET_MERCHANT_OFFERS_SQL, values=query_values
        )
        return [MerchantOfferMerchantView(**offer) for offer in offers]

    # TODO: TRANSIENT - not currently used in application, only in test suite
    async def get_merchant_offer_(
        self, *, merchant_offer_id: uuid.UUID
    ) -> List[MerchantOfferDBModel]:
        sql = """
            SELECT * FROM merchant_offers WHERE id = :merchant_offer_id;
        """
        query_values = {"merchant_offer_id": merchant_offer_id}
        offers = await self.db.fetch_all(query=sql, values=query_values)
        return [MerchantOfferDBModel(**offer) for offer in offers]

    async def create_merchant_offer(
        self, *, merchant_offer_new: MerchantOfferNew
    ) -> Optional[NewRecordResponse]:
        offer = await self.db.fetch_one(
            query=CREATE_MERCHANT_OFFER_SQL, values=merchant_offer_new.dict()
        )
        return None if offer is None else NewRecordResponse(**offer)

    async def update_merchant_offer(
        self, *, merchant_offer_update_request: MerchantOfferUpdateRequest
    ) -> Optional[UpdatedRecordResponse]:
        offer = await self.db.fetch_one(
            query=UPDATE_MERCHANT_OFFER_SQL, values=merchant_offer_update_request.dict()
        )
        return None if offer is None else UpdatedRecordResponse(**offer)

    async def update_merchant_offer_status(
        self, *, id: uuid.UUID, status: str
    ) -> Optional[UpdatedRecordResponse]:
        offer = await self.db.fetch_one(
            query=UPDATE_MERCHANT_OFFER_STATUS_SQL, values={"id": id, "status": status}
        )
        return None if offer is None else UpdatedRecordResponse(**offer)

    async def is_merchant_offer_updateable(
        self,
        *,
        id: uuid.UUID,
        merchant_id: uuid.UUID,
    ) -> BooleanResponse:
        offer = await self.db.fetch_one(
            query=IS_MERCHANT_OFFER_UPDATEABLE_SQL,
            values={
                "id": id,
                "merchant_id": merchant_id,
            },
        )
        return BooleanResponse(**offer)
