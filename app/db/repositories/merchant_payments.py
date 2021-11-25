from typing import Optional

from app.db.repositories.base import BaseRepository
from app.models.core import IDModelMixin
from app.models.merchant_payment import (MerchantPayment, MerchantPaymentNew,
                                         MerchantPaymentUpdate)

NEW_MERCHANT_PAYMENT_SQL = """
    INSERT INTO merchant_payments(merchant_id, amount, payment_identifier, status)
    VALUES(:merchant_id, :amount, :payment_identifier, :status)
    RETURNING id
"""


GET_MERCHANT_PAYMENT_BY_IDENTIFIER_SQL = """
    SELECT id, merchant_id, amount, payment_identifier, status FROM merchant_payments
    WHERE payment_identifier = :payment_identifier
"""


UPDATE_MERCHANT_PAYMENT_STATUS_SQL = """
    UPDATE merchant_payments SET status = :status
    WHERE id = :id
    RETURNING id, merchant_id, amount, payment_identifier, status
"""


class MerchantPaymentsRepository(BaseRepository):
    async def create_merchant_payment(
        self, *, new_merchant_payment: MerchantPaymentNew
    ) -> Optional[IDModelMixin]:
        query_values = new_merchant_payment.dict()
        created_merchant_payment = await self.db.fetch_one(
            query=NEW_MERCHANT_PAYMENT_SQL, values=query_values
        )
        return (
            None
            if created_merchant_payment is None
            else IDModelMixin(**created_merchant_payment)
        )

    async def get_merchant_payment_by_identifier(
        self, *, payment_identifier: str
    ) -> Optional[MerchantPayment]:
        query_values = {
            "payment_identifier": payment_identifier,
        }
        merchant_payment = await self.db.fetch_one(
            query=GET_MERCHANT_PAYMENT_BY_IDENTIFIER_SQL, values=query_values
        )
        return None if merchant_payment is None else MerchantPayment(**merchant_payment)

    async def update_merchant_payment_status(
        self,
        *,
        merchant_payment_update: MerchantPaymentUpdate,
    ) -> Optional[MerchantPayment]:
        query_values = merchant_payment_update.dict()
        merchant_payment = await self.db.fetch_one(
            query=UPDATE_MERCHANT_PAYMENT_STATUS_SQL, values=query_values
        )
        return None if merchant_payment is None else MerchantPayment(**merchant_payment)
