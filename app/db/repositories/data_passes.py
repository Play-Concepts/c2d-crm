import uuid
from typing import List

from app.models.data_pass import DataPassCustomerView, DataPassMerchantView

from ...models.core import IDModelMixin
from .base import BaseRepository

GET_CUSTOMER_DATA_PASSES_SQL = """
    SELECT data_passes.id, data_passes.name, data_passes.title, data_passes.description_for_merchants,
    data_passes.description_for_customers, data_passes.perks_url_for_merchants, data_passes.perks_url_for_customers,
    sources.name source_name, sources.description source_description, sources.logo_url source_logo_url,
    verifiers.name verifier_name, verifiers.description verifier_description, verifiers.logo_url verifier_logo_url,
    (select status from data_pass_activations where pda_url=:pda_url and data_pass_id=data_passes.id)
    AS activation_status FROM data_passes
    JOIN data_pass_sources sources ON (data_passes.data_pass_source_id=sources.id)
    JOIN data_pass_sources verifiers ON (data_passes.data_pass_verifier_id=verifiers.id)
    ORDER BY data_passes.title;
"""

GET_MERCHANT_DATA_PASSES_SQL = """
    SELECT data_passes.id, data_passes.name, data_passes.title, data_passes.description_for_merchants,
    data_passes.description_for_customers, data_passes.perks_url_for_merchants, data_passes.perks_url_for_customers,
    data_passes.currency_code, data_passes.price,
    sources.name source_name, sources.description source_description, sources.logo_url source_logo_url,
    verifiers.name verifier_name, verifiers.description verifier_description, verifiers.logo_url verifier_logo_url,
    data_passes.status FROM data_passes
    JOIN data_pass_sources sources ON (data_passes.data_pass_source_id=sources.id)
    JOIN data_pass_sources verifiers ON (data_passes.data_pass_verifier_id=verifiers.id)
    ORDER BY data_passes.title;
"""

ACTIVATE_DATA_PASS_SQL = """
    INSERT INTO data_pass_activations(data_pass_id, pda_url) VALUES(:data_pass_id, :pda_url)
    ON CONFLICT (data_pass_id, pda_url)
    DO UPDATE SET status='active', updated_at=now()
    RETURNING id;
"""


class DataPassesRepository(BaseRepository):
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

    async def activate_data_pass(
        self, *, data_pass_id: uuid.UUID, pda_url: str
    ) -> IDModelMixin:
        query_values = {"data_pass_id": data_pass_id, "pda_url": pda_url}
        data_activation = await self.db.fetch_one(
            query=ACTIVATE_DATA_PASS_SQL, values=query_values
        )
        return IDModelMixin(**data_activation)

    # TODO: TRANSIENT - not currently used in application, only in test suite
    async def create_data_pass_source_(
        self,
        *,
        name: str,
        description: str,
        logo_url: str,
        is_data_source: bool,
        is_data_verifier: bool,
    ) -> IDModelMixin:
        sql = """
            INSERT INTO data_pass_sources(name, description, logo_url, is_data_source, is_data_verifier)
            VALUES(:name, :description, :logo_url, :is_data_source, :is_data_verifier)
            RETURNING id
            """
        query_values = {
            "name": name,
            "description": description,
            "logo_url": logo_url,
            "is_data_source": is_data_source,
            "is_data_verifier": is_data_verifier,
        }
        data_pass_source = await self.db.fetch_one(query=sql, values=query_values)
        return IDModelMixin(**data_pass_source)

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
    ):
        sql = """
            INSERT INTO data_passes(name, title, description_for_merchants, description_for_customers,
            perks_url_for_merchants, perks_url_for_customers, data_pass_source_id,
            data_pass_verifier_id, currency_code, price, status)
            VALUES(:name, :title, :description_for_merchants, :description_for_customers,
            :perks_url_for_merchants, :perks_url_for_customers, :data_pass_source_id,
            :data_pass_verifier_id, :currency_code, :price, :status)
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
        }
        data_pass = await self.db.fetch_one(query=sql, values=query_values)
        return IDModelMixin(**data_pass)
