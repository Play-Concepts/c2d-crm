from app.models.core import BooleanResponse
from app.models.customer_log import CustomerLog, CustomerLogNew

from .base import BaseRepository

NEW_CUSTOMER_LOG_SQL = """
    INSERT INTO customers_log(pda_url, event) VALUES(:pda_url, :event)
    RETURNING id, created_at;
"""


CHECK_FIRST_LOGIN_CUSTOMER_SQL = """
    SELECT NOT EXISTS(SELECT 1 FROM customers_log WHERE pda_url=:pda_url) AS value;
"""


class CustomersLogRepository(BaseRepository):
    async def log_event(self, *, customer_log_new: CustomerLogNew) -> CustomerLog:
        query_values = customer_log_new.dict()

        created_customer_log = await self.db.fetch_one(
            query=NEW_CUSTOMER_LOG_SQL, values=query_values
        )
        return CustomerLog(**created_customer_log)

    async def customer_exists(self, *, pda_url: str) -> BooleanResponse:
        response = await self.db.fetch_one(
            query=CHECK_FIRST_LOGIN_CUSTOMER_SQL, values={"pda_url": pda_url}
        )
        return BooleanResponse(**response)
