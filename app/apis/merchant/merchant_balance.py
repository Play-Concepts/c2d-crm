import uuid
from typing import Optional

from app.db.repositories.merchant_balances import MerchantBalancesRepository
from app.models.merchant_balance import MerchantBalanceAmount


async def fn_has_credit(
    email: str, merchant_balances_repo: MerchantBalancesRepository
) -> bool:
    balance_amount = await fn_get_merchant_balance_amount_by_email(
        email, merchant_balances_repo
    )
    return False if balance_amount is None else balance_amount.amount > 0


async def fn_get_merchant_balance_amount(
    merchant_id: uuid.UUID, merchant_balances_repo: MerchantBalancesRepository
) -> Optional[MerchantBalanceAmount]:
    return merchant_balances_repo.get_merchant_balance_amount(merchant_id=merchant_id)


async def fn_get_merchant_balance_amount_by_email(
    email: str, merchant_balances_repo: MerchantBalancesRepository
) -> Optional[MerchantBalanceAmount]:
    return merchant_balances_repo.get_merchant_balance_amount_by_email(email=email)
