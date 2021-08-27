import json
import uuid
from typing import List, Optional

from app.models.customer import (CustomerBasicView, CustomerClaimResponse,
                                 CustomerNew, CustomerView)

from .base import BaseRepository

NEW_CUSTOMER_SQL = """
    INSERT INTO customers(data, pda_url, status) VALUES(:data, :pda_url, :status) RETURNING id;
"""

VIEW_CUSTOMER_SQL = """
    SELECT id, data, pda_url, status FROM customers WHERE id = :id;
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
    SELECT id, claimed_timestamp FROM customers WHERE pda_url = :pda_url;
"""

SEARCH_CUSTOMER_SQL = """
    SELECT id, data, pda_url, status FROM customers WHERE
    data->'person'->'profile'->>'last_name' ilike :last_name AND
    data->'person'->'address'->>'address_line_1' ilike :address AND
    data->'person'->'contact'->>'email' ilike :email AND
    status='new';
"""

CLAIM_DATA_SQL = """
    UPDATE customers SET status='claimed',
    claimed_timestamp=now(),
    pda_url=:pda_url,
    updated_at=now()
    WHERE id=:id
    RETURNING id, data, status, pda_url, claimed_timestamp;
"""


class CustomersRepository(BaseRepository):
    async def create_customer(self, *, new_customer: CustomerNew) -> CustomerView:
        query_values = new_customer.dict()
        query_values["data"] = json.dumps(new_customer.data)

        created_customer = await self.db.fetch_one(
            query=NEW_CUSTOMER_SQL, values=query_values
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

    async def get_customer(self, *, customer_id: uuid.UUID) -> Optional[CustomerView]:
        customer = await self.db.fetch_one(
            query=VIEW_CUSTOMER_SQL, values={"id": customer_id}
        )
        return None if customer is None else CustomerView(**customer)

    async def get_customer_basic(self, *, pda_url: str) -> Optional[CustomerBasicView]:
        customer = await self.db.fetch_one(
            query=VIEW_CUSTOMER_BASIC_SQL, values={"pda_url": pda_url}
        )
        return None if customer is None else CustomerBasicView(**customer)

    async def search_customers(
        self, *, last_name: str, address: str, email: str
    ) -> List[CustomerView]:
        def param_format(element: str) -> str:
            return "" if element == "" or element is None else element.strip()

        values = {
            "last_name": param_format(last_name),
            "address": param_format(address),
            "email": param_format(email),
        }
        customers = await self.db.fetch_all(query=SEARCH_CUSTOMER_SQL, values=values)
        customers_list = [CustomerView(**customer) for customer in customers]
        if len(customers_list) == 1 and customers_list[0].total_count == 0:
            return []
        return customers_list

    async def claim_data(
        self, *, identifier: uuid.UUID, pda_url: str
    ) -> Optional[CustomerClaimResponse]:
        customer = await self.db.fetch_one(
            query=CLAIM_DATA_SQL,
            values={
                "id": identifier,
                "pda_url": pda_url,
            },
        )
        return None if customer is None else CustomerClaimResponse(**customer)
