import json
import uuid
from typing import List, Optional

from pydantic.types import Json

from app.models.customer import (CustomerBasicView, CustomerClaimResponse,
                                 CustomerNew, CustomerView)

from .base import BaseRepository

NEW_CUSTOMER_SQL = """
    INSERT INTO {data_table}(data, data_hash, pda_url, status)
    VALUES(:data, :data_hash, :pda_url, :status)
    ON CONFLICT(data_hash) DO NOTHING
    RETURNING id;
"""

VIEW_CUSTOMER_SQL = """
    SELECT id, data, pda_url, status FROM {data_table} WHERE id = :id;
"""

VIEW_CUSTOMER_BASIC_SQL = """
    SELECT id, claimed_timestamp FROM {data_table} WHERE pda_url = :pda_url
"""

CLAIM_DATA_SQL = """
    UPDATE {data_table} SET status='claimed',
    claimed_timestamp=now(),
    pda_url=:pda_url,
    updated_at=now()
    WHERE id=:id
    RETURNING id, data, status, pda_url, claimed_timestamp;
"""


class CustomersRepository(BaseRepository):
    async def create_customer(
        self, *, new_customer: CustomerNew, data_table: str
    ) -> CustomerView:
        query_values = new_customer.dict()
        query_values["data"] = json.dumps(new_customer.data)

        created_customer = await self.db.fetch_one(
            query=NEW_CUSTOMER_SQL.format(data_table=data_table), values=query_values
        )
        return None if created_customer is None else CustomerView(**created_customer)

    async def get_customer(
        self, *, customer_id: uuid.UUID, data_table: str
    ) -> Optional[CustomerView]:
        customer = await self.db.fetch_one(
            query=VIEW_CUSTOMER_SQL.format(data_table=data_table),
            values={"id": customer_id},
        )
        return None if customer is None else CustomerView(**customer)

    async def get_customer_basic(
        self, *, pda_url: str, data_table: str
    ) -> Optional[CustomerBasicView]:
        customer = await self.db.fetch_one(
            query=VIEW_CUSTOMER_BASIC_SQL.format(data_table=data_table),
            values={"pda_url": pda_url},
        )
        return None if customer is None else CustomerBasicView(**customer)

    async def search_customers(
        self, *, data_table: str, search_sql: str, search_params: Json
    ) -> List[CustomerView]:
        values = search_params
        customers = await self.db.fetch_all(
            query=search_sql.format(data_table=data_table), values=values
        )
        return [CustomerView(**customer) for customer in customers]

    async def claim_data(
        self, *, data_table: str, identifier: uuid.UUID, pda_url: str
    ) -> Optional[CustomerClaimResponse]:
        customer = await self.db.fetch_one(
            query=CLAIM_DATA_SQL.format(data_table=data_table),
            values={
                "id": identifier,
                "pda_url": pda_url,
            },
        )
        return None if customer is None else CustomerClaimResponse(**customer)
