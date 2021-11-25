from typing import Optional

from app.db.repositories.base import BaseRepository
from app.models.lookup_payment_balance import LookupPaymentBalance

GET_LOOKUP_PAYMENT_BALANCE_SQL = """
    SELECT currency, amount, creditable_balance FROM lookup_payment_balances
    WHERE currency ilike :currency
"""


class LookupPaymentBalancesRepository(BaseRepository):
    async def get_lookup_payment_balance(
        self,
        *,
        currency: str,
    ) -> Optional[LookupPaymentBalance]:
        query_values = {
            "currency": currency,
        }
        lookup_payment_balance = await self.db.fetch_one(
            query=GET_LOOKUP_PAYMENT_BALANCE_SQL, values=query_values
        )
        return (
            None
            if lookup_payment_balance is None
            else LookupPaymentBalance(**lookup_payment_balance)
        )
