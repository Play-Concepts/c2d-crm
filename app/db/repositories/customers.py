import json
import uuid
from typing import List, Optional

from pydantic.types import Json

from app.models.customer import (CustomerBasicView, CustomerClaimResponse,
                                 CustomerNew, CustomerView)

from .base import BaseRepository

NEW_CUSTOMER_SQL = """
    INSERT INTO {data_table}(data, pda_url, status)
    VALUES(:data, :pda_url, :status) RETURNING id;
"""

VIEW_CUSTOMER_SQL = """
    SELECT id, data, pda_url, status FROM {data_table} WHERE id = :id;
"""

GET_CUSTOMERS_SQL = """
    WITH cte AS (SELECT id, data, pda_url, status FROM customers
    ORDER BY data->'person'->'profile'->>'last_name', data->'person'->'profile'->>'first_name')
    SELECT * FROM (
        TABLE cte
        LIMIT :limit
        OFFSET :offset
    ) sub
    RIGHT  JOIN (SELECT count(*) FROM cte) c(total_count) ON true;
"""

VIEW_CUSTOMER_BASIC_SQL = """
    SELECT id, claimed_timestamp FROM customers WHERE pda_url = :pda_url
    AND data_pass_id = :data_pass_id;
"""

SEARCH_CUSTOMER_SQL = """
    SELECT id, data, pda_url, status FROM customers WHERE
    data_pass_id = :data_pass_id AND
    data->'person'->'profile'->>'last_name' ilike :last_name AND
    data->'person'->'address'->>'address_line_1' ilike :address AND
    (data->'person'->'contact'->>'email' ilike :email OR
    data->'person'->'contact'->>'email_1' ilike :email OR
    data->'person'->'contact'->>'email_2' ilike :email OR
    data->'person'->'contact'->>'email_3' ilike :email OR
    data->'person'->'contact'->>'email_4' ilike :email OR
    data->'person'->'contact'->>'email_5' ilike :email) AND
    status='new';
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
        return CustomerView(**created_customer)

    async def get_customers(self, *, offset: int, limit: int) -> List[CustomerView]:
        customers = await self.db.fetch_all(
            query=GET_CUSTOMERS_SQL, values={"offset": offset, "limit": limit}
        )
        customers_list = [CustomerView(**customer) for customer in customers]
        if len(customers_list) == 1 and customers_list[0].total_count == 0:
            return []
        return customers_list

    async def get_customer(
        self, *, customer_id: uuid.UUID, data_table: str
    ) -> Optional[CustomerView]:
        customer = await self.db.fetch_one(
            query=VIEW_CUSTOMER_SQL.format(data_table=data_table),
            values={"id": customer_id},
        )
        return None if customer is None else CustomerView(**customer)

    async def get_customer_basic(
        self, *, data_pass_id: uuid.UUID, pda_url: str
    ) -> Optional[CustomerBasicView]:
        customer = await self.db.fetch_one(
            query=VIEW_CUSTOMER_BASIC_SQL,
            values={"pda_url": pda_url, "data_pass_id": data_pass_id},
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
