import uuid
from typing import Optional, List

from .base import BaseRepository
from app.models.customer import CustomerNew, CustomerView
import json


NEW_CUSTOMER_SQL = """
    INSERT INTO customers(id, data, pda_url, status) VALUES(:id, :data, :pda_url, :status) RETURNING id;
"""

VIEW_CUSTOMER_SQL = """
    SELECT id, data, pda_url, status FROM customers WHERE id = :id
"""

GET_CUSTOMERS_SQL = """
    SELECT id, data, pda_url, status FROM customers OFFSET :offset LIMIT :limit
"""


class CustomersRepository(BaseRepository):
    async def create_customer(self, *, new_customer: CustomerNew) -> CustomerView:
        query_values = new_customer.dict()
        query_values['id']=uuid.uuid4()
        query_values['data'] = json.dumps(new_customer.data)

        created_customer = await self.db.fetch_one(query=NEW_CUSTOMER_SQL, values=query_values)

        return CustomerView(**created_customer)

    async def get_customer(self, *, customer_id: uuid.UUID) -> Optional[CustomerView]:
        customer = await self.db.fetch_one(query=VIEW_CUSTOMER_SQL, values={"id": customer_id})

        return None if customer is None else CustomerView(**customer)

    async def get_customers(self, *, offset: int, limit: int) -> List[CustomerView]:
        customers = await self.db.fetch_all(query=GET_CUSTOMERS_SQL, values={"offset": offset, "limit": limit})

        return [CustomerView(**customer) for customer in customers]
