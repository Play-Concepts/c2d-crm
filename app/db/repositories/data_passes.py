import uuid
from typing import List, Optional

from app.models.core import BooleanResponse, Count, IDModelMixin
from app.models.data_pass import (DataPassBasicView, DataPassCustomerView,
                                  DataPassMerchantView)

from .base import BaseRepository

GET_DATA_PASS_SQL = """
    SELECT id, name FROM data_passes
    WHERE id = :data_pass_id;
"""

GET_CUSTOMER_DATA_PASSES_SQL = """
    SELECT data_passes.id, data_passes.name, data_passes.title, data_passes.description_for_merchants,
    data_passes.description_for_customers, data_passes.perks_url_for_merchants, data_passes.perks_url_for_customers,
    data_passes.details_url, (select updated_at from data_pass_activations where pda_url=:pda_url and
    data_pass_id=data_passes.id) + data_passes.expiry_days * INTERVAL '1 day' AS expiry_date, data_passes.expiry_days,
    sources.name source_name, sources.description source_description, sources.logo_url source_logo_url,
    verifiers.name verifier_name, verifiers.description verifier_description, verifiers.logo_url verifier_logo_url,
    (select status from data_pass_activations where pda_url=:pda_url and data_pass_id=data_passes.id)
    AS activation_status FROM data_passes
    JOIN data_pass_sources sources ON (data_passes.data_pass_source_id=sources.id)
    JOIN data_pass_verifiers verifiers ON (data_passes.data_pass_verifier_id=verifiers.id)
    ORDER BY data_passes.title;
"""

GET_MERCHANT_DATA_PASSES_SQL = """
    SELECT data_passes.id, data_passes.name, data_passes.title, data_passes.description_for_merchants,
    data_passes.description_for_customers, data_passes.perks_url_for_merchants, data_passes.perks_url_for_customers,
    data_passes.currency_code, data_passes.price, data_passes.details_url, data_passes.expiry_days,
    sources.name source_name, sources.description source_description, sources.logo_url source_logo_url,
    verifiers.name verifier_name, verifiers.description verifier_description, verifiers.logo_url verifier_logo_url,
    data_passes.status FROM data_passes
    JOIN data_pass_sources sources ON (data_passes.data_pass_source_id=sources.id)
    JOIN data_pass_verifiers verifiers ON (data_passes.data_pass_verifier_id=verifiers.id)
    ORDER BY data_passes.title;
"""

ACTIVATE_DATA_PASS_SQL = """
    INSERT INTO data_pass_activations(data_pass_id, pda_url, updated_at) VALUES(:data_pass_id, :pda_url, now())
    ON CONFLICT (data_pass_id, pda_url)
    DO UPDATE SET status='active', updated_at=now()
    RETURNING id;
"""

IS_DATA_PASS_VALID_SQL = """
    SELECT COUNT(id) FROM data_passes WHERE id=:data_pass_id AND status='active';
"""


IS_DATA_PASS_EXPIRED_SQL = """
    SELECT data_pass_activations.updated_at + data_passes.expiry_days * INTERVAL '1 day' < now() AS value
    FROM data_pass_activations JOIN data_passes
    ON (data_pass_activations.data_pass_id=data_passes.id)
    WHERE data_pass_activations.data_pass_id=:data_pass_id AND pda_url=:pda_url;
"""


class DataPassesRepository(BaseRepository):
    async def get_data_pass(
        self, *, data_pass_id: uuid.UUID
    ) -> Optional[DataPassBasicView]:
        query_values = {"data_pass_id": data_pass_id}
        data_pass = await self.db.fetch_one(
            query=GET_DATA_PASS_SQL, values=query_values
        )
        return None if data_pass is None else DataPassBasicView(**data_pass)

    async def get_customer_data_passes(
        self, *, pda_url: str
    ) -> List[DataPassCustomerView]:
        query_values = {"pda_url": pda_url}
        data_passes = await self.db.fetch_all(
            query=GET_CUSTOMER_DATA_PASSES_SQL, values=query_values
        )
        return [DataPassCustomerView(**data_pass) for data_pass in data_passes]

    async def get_merchant_data_passes(self) -> List[DataPassMerchantView]:
        data_passes = await self.db.fetch_all(
            query=GET_MERCHANT_DATA_PASSES_SQL, values={}
        )
        return [DataPassMerchantView(**data_pass) for data_pass in data_passes]

    async def is_data_pass_valid(self, *, data_pass_id: uuid.UUID) -> bool:
        count = await self.db.fetch_one(
            query=IS_DATA_PASS_VALID_SQL, values={"data_pass_id": data_pass_id}
        )
        return Count(**count).count == 1

    async def is_data_pass_expired(
        self, *, pda_url: Optional[str], data_pass_id: Optional[uuid.UUID]
    ) -> bool:
        if pda_url is None or data_pass_id is None:
            return False

        is_expired = await self.db.fetch_one(
            query=IS_DATA_PASS_EXPIRED_SQL,
            values={"pda_url": pda_url, "data_pass_id": data_pass_id},
        )
        return False if is_expired is None else BooleanResponse(**is_expired).value

    async def activate_data_pass(
        self, *, data_pass_id: uuid.UUID, pda_url: str
    ) -> IDModelMixin:
        query_values = {"data_pass_id": data_pass_id, "pda_url": pda_url}
        data_activation = await self.db.fetch_one(
            query=ACTIVATE_DATA_PASS_SQL, values=query_values
        )
        return IDModelMixin(**data_activation)

    # TODO: TRANSIENT - not currently used in application, only in test suite
    async def create_data_pass_(
        self,
        *,
        name: str,
        title: str,
        description_for_merchants: str,
        description_for_customers: str,
        perks_url_for_merchants: str,
        perks_url_for_customers: str,
        data_pass_source_id: uuid.UUID,
        data_pass_verifier_id: uuid.UUID,
        currency_code: str,
        price: float,
        status: str,
        expiry_days: int,
    ):
        sql = """
            INSERT INTO data_passes(name, title, description_for_merchants, description_for_customers,
            perks_url_for_merchants, perks_url_for_customers, data_pass_source_id,
            data_pass_verifier_id, currency_code, price, status, expiry_days)
            VALUES(:name, :title, :description_for_merchants, :description_for_customers,
            :perks_url_for_merchants, :perks_url_for_customers, :data_pass_source_id,
            :data_pass_verifier_id, :currency_code, :price, :status, :expiry_days)
            RETURNING id
        """
        query_values = {
            "name": name,
            "title": title,
            "description_for_merchants": description_for_merchants,
            "description_for_customers": description_for_customers,
            "perks_url_for_merchants": perks_url_for_merchants,
            "perks_url_for_customers": perks_url_for_customers,
            "data_pass_source_id": data_pass_source_id,
            "data_pass_verifier_id": data_pass_verifier_id,
            "currency_code": currency_code,
            "price": price,
            "status": status,
            "expiry_days": expiry_days,
        }
        data_pass = await self.db.fetch_one(query=sql, values=query_values)
        return IDModelMixin(**data_pass)

    # TODO: TRANSIENT - not currently used in application, only in test suite
    async def get_random_data_pass_(
        self,
    ):
        sql = """
            SELECT id FROM data_passes
            ORDER BY random() LIMIT 1
        """
        data_pass = await self.db.fetch_one(query=sql, values={})
        return IDModelMixin(**data_pass)

    # TODO: TRANSIENT - not currently used in application, only in test suite
    async def expire_data_pass_(
        self, *, data_pass_id: uuid.UUID, pda_url: str
    ) -> IDModelMixin:
        sql = """
            UPDATE data_pass_activations SET updated_at = updated_at - interval '2 years'
            WHERE data_pass_id=:data_pass_id AND pda_url=:pda_url RETURNING id;
        """
        query_values = {"data_pass_id": data_pass_id, "pda_url": pda_url}
        data_activation = await self.db.fetch_one(query=sql, values=query_values)
        return IDModelMixin(**data_activation)
