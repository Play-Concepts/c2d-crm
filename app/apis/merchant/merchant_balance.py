import uuid
from typing import Optional, Union

from fastapi import Response, status

from app.db.repositories.merchant_balances import MerchantBalancesRepository
from app.db.repositories.merchants import MerchantsRepository
from app.models.core import NewRecordResponse, NotFound
from app.models.merchant_balance import (MerchantBalanceAmount,
                                         MerchantBalanceNew)


async def fn_has_credit(
    merchant_id: uuid.UUID,
    minimum_amount: int,
    merchant_balances_repo: MerchantBalancesRepository,
) -> bool:
    balance_amount = await fn_get_merchant_balance_amount(
        merchant_id, merchant_balances_repo
    )
    return False if balance_amount is None else balance_amount.amount > minimum_amount


async def fn_get_merchant_balance_amount(
    merchant_email: str,
    merchants_repository: MerchantsRepository,
    merchant_balances_repo: MerchantBalancesRepository,
    response: Response,
) -> Union[NotFound, MerchantBalanceAmount]:
    merchant = await merchants_repository.get_merchant_by_email(email=merchant_email)
    if merchant is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFound(message="Merchant Not Found")

    return await merchant_balances_repo.get_merchant_balance_amount(
        merchant_id=merchant.id
    )


async def fn_debit_merchant_balance(
    merchant_id: uuid.UUID,
    amount: int,
    transaction_identifier: Optional[uuid.UUID],
    merchant_balances_repo: MerchantBalancesRepository,
) -> Optional[NewRecordResponse]:
    return await merchant_balances_repo.create_merchant_balance(
        new_merchant_balance=MerchantBalanceNew(
            merchant_id=merchant_id,
            amount=amount,
            transaction_identifier=transaction_identifier,
            balance_type="debit",
        )
    )
