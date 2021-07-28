from .base import BaseRepository
from app.models.core import IDModelMixin, BooleanResponse
from app.models.customer_log import CustomerLogNew


NEW_CUSTOMER_LOG_SQL="""
    INSERT INTO customers_log(id, pda_url, event, created_at) VALUES(:id, :pda_url, :event, :created_at) 
    RETURNING id;
"""


CHECK_FIRST_LOGIN_CUSTOMER_SQL="""
    SELECT EXISTS(SELECT 1 FROM customers_log WHERE pda_url=:pda_url) AS value;
"""


class CustomersLogRepository(BaseRepository):
    async def log_event(self, *, customer_log_new:CustomerLogNew) -> IDModelMixin:
        query_values = customer_log_new.dict()

        created_customer_log = await self.db.fetch_one(query=NEW_CUSTOMER_LOG_SQL, values=query_values)
        return IDModelMixin(**created_customer_log)

    async def customer_exists(self, *, pda_url: str) -> BooleanResponse:
        response = await self.db.fetch_one(query=CHECK_FIRST_LOGIN_CUSTOMER_SQL, values={"pda_url": pda_url})
        return BooleanResponse(**response)