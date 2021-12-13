import uuid
from typing import Optional

from app.db.repositories.base import BaseRepository
from app.models.core import NewRecordResponse
from app.models.merchant_balance import (MerchantBalanceAmount,
                                         MerchantBalanceNew)

NEW_MERCHANT_BALANCE_SQL = """
    INSERT INTO merchant_balances(merchant_id, amount, balance_type, transaction_identifier)
    VALUES(:merchant_id, :amount, :balance_type, :transaction_identifier)
    RETURNING id, created_at;
"""


GET_MERCHANT_BALANCE_AMOUNT_SQL = """
    SELECT SUM(amount) AS amount FROM
    (SELECT CASE WHEN balance_type='credit' THEN amount
    ELSE amount * (-1) END AS amount FROM merchant_balances
    WHERE merchant_id = :merchant_id) AS cred_deb
"""


class MerchantBalancesRepository(BaseRepository):
    async def create_merchant_balance(
        self, *, new_merchant_balance: MerchantBalanceNew
    ) -> Optional[NewRecordResponse]:
        query_values = new_merchant_balance.dict()
        created_merchant_balance = await self.db.fetch_one(
            query=NEW_MERCHANT_BALANCE_SQL, values=query_values
        )
        return (
            None
            if created_merchant_balance is None
            else NewRecordResponse(**created_merchant_balance)
        )

    async def get_merchant_balance_amount(
        self,
        *,
        merchant_id: uuid.UUID,
    ) -> MerchantBalanceAmount:
        query_values = {
            "merchant_id": merchant_id,
        }
        merchant_balance = await self.db.fetch_one(
            query=GET_MERCHANT_BALANCE_AMOUNT_SQL, values=query_values
        )
        return (
            MerchantBalanceAmount(amount=0)
            if merchant_balance is None or merchant_balance["amount"] is None
            else MerchantBalanceAmount(**merchant_balance)
        )
