import uuid
from typing import Optional, List

from .base import BaseRepository
from app.models.customer import CustomerNew, CustomerView, CustomerBasicView, CustomerClaimResponse
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

VIEW_CUSTOMER_BASIC_SQL = """
    SELECT id FROM customers WHERE pda_url = :pda_url
"""

SEARCH_CUSTOMER_SQL = """
    SELECT id, data, pda_url, status FROM customers WHERE 
    data->'person'->'profile'->>'last_name' ilike :last_name AND
    data->'person'->'address'->>'address_line_1' ilike :house_number AND 
    data->'person'->'contact'->>'email' ilike :email AND 
    status='new'
"""

CLAIM_DATA_SQL = """
    UPDATE customers SET status='claimed', 
    pda_url=:pda_url 
    WHERE id=:id 
    RETURNING id, status, pda_url;
"""


class CustomersRepository(BaseRepository):
    async def create_customer(self, *, new_customer: CustomerNew) -> CustomerView:
        query_values = new_customer.dict()
        query_values['id']=uuid.uuid4()
        query_values['data'] = json.dumps(new_customer.data)

        created_customer = await self.db.fetch_one(query=NEW_CUSTOMER_SQL, values=query_values)
        return CustomerView(**created_customer)

    async def get_customers(self, *, offset: int, limit: int) -> List[CustomerView]:
        customers = await self.db.fetch_all(query=GET_CUSTOMERS_SQL, values={"offset": offset, "limit": limit})
        return [CustomerView(**customer) for customer in customers]

    async def get_customer(self, *, customer_id: uuid.UUID) -> Optional[CustomerView]:
        customer = await self.db.fetch_one(query=VIEW_CUSTOMER_SQL, values={"id": customer_id})
        return None if customer is None else CustomerView(**customer)

    async def get_customer_basic(self, *, pda_url: str) -> Optional[CustomerBasicView]:
        customer = await self.db.fetch_one(query=VIEW_CUSTOMER_BASIC_SQL, values={"pda_url": pda_url})
        return None if customer is None else CustomerBasicView(**customer)

    async def search_customers(self, *, last_name: str, house_number:str, email: str) -> List[CustomerView]:
        def param_format(element: str) -> str:
            return '' if element == '' or element is None else "{}%".format(element)

        values = {
            "last_name": param_format(last_name),
            "house_number": param_format(house_number),
            "email": param_format(email)
        }
        customers = await self.db.fetch_all(query=SEARCH_CUSTOMER_SQL, values=values)
        return [CustomerView(**customer) for customer in customers]

    async def claim_data(self, *, identifier: uuid.UUID, pda_url: str) -> Optional[CustomerClaimResponse]:
        customer = await self.db.fetch_one(query=CLAIM_DATA_SQL, values={"id": identifier, "pda_url": pda_url})
        return None if customer is None else CustomerClaimResponse(**customer)
