import json
import uuid
from datetime import datetime
from typing import Callable, List, Optional

from pydantic.types import Json

from app.models.customer import (CustomerClaimResponse, CustomerNew,
                                 CustomerView)

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

DATA_TO_CLAIM = """
    SELECT id, data, status, pda_url, claimed_timestamp FROM {data_table}
    WHERE id=:id AND status='new'
"""

CLAIM_DATA_SQL = """
    UPDATE {data_table} SET status='claimed',
    claimed_timestamp=:claimed_timestamp,
    data={data},
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

    async def search_customers(
        self,
        *,
        data_table: str,
        search_sql: str,
        transformer: Callable,
        search_params: Json,
    ) -> List[CustomerView]:
        values = {key: value.strip() for (key, value) in search_params.items()}
        customers = await self.db.fetch_all(
            query=search_sql.format(data_table=data_table), values=values
        )
        return [transformer(CustomerView(**customer)) for customer in customers]

    async def claim_data(
        self,
        *,
        data_table: str,
        identifier: uuid.UUID,
        pda_url: str,
        claimed_timestamp: datetime,
    ) -> Optional[CustomerClaimResponse]:
        customer = await self.db.fetch_one(
            query=CLAIM_DATA_SQL.format(data_table=data_table, data="'{}'"),
            values={
                "id": identifier,
                "pda_url": pda_url,
                "claimed_timestamp": claimed_timestamp,
            },
        )
        return None if customer is None else CustomerClaimResponse(**customer)

    async def data_to_claim(
        self, *, data_table: str, identifier: uuid.UUID
    ) -> Optional[CustomerClaimResponse]:
        customer = await self.db.fetch_one(
            query=DATA_TO_CLAIM.format(data_table=data_table),
            values={
                "id": identifier,
            },
        )
        return None if customer is None else CustomerClaimResponse(**customer)
