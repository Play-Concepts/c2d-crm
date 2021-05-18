import uuid

from .base import BaseRepository
from app.models.customer import CustomerNew, CustomerView
import json


NEW_CUSTOMER_SQL = """
    INSERT INTO customers(id, data, pda_url, status) VALUES(:id, :data, :pda_url, :status)
    RETURNING id, data::text, pda_url, status;
"""


class CustomersRepository(BaseRepository):
    async def create_customer(self, *, new_customer: CustomerNew) -> CustomerView:
        query_values = new_customer.dict()
        query_values['id']=uuid.uuid4()
        query_values['data'] = json.dumps(new_customer.data)

        created_customer = await self.db.fetch_one(query=NEW_CUSTOMER_SQL, values=query_values)

        return CustomerView(**created_customer)
