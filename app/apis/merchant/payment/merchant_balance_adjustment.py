import uuid
from datetime import datetime

from dateutil.relativedelta import relativedelta

from app.core.global_config import config as app_config
from app.db.repositories.data_passes import DataPassesRepository
from app.db.repositories.merchant_balances import MerchantBalancesRepository
from app.db.repositories.merchant_offers_data_passes import \
    MerchantOffersDataPassesRepository
from app.models.merchant_balance import MerchantBalanceNew


async def charge_new_merchant_offers_data_passes(
    merchant_id: uuid.UUID,
    merchant_offer_id: uuid.UUID,
    data_passes_repo: DataPassesRepository,
    merchant_balances_repo: MerchantBalancesRepository,
    merchant_offers_data_passes_repo: MerchantOffersDataPassesRepository,
) -> int:
    today, last_day = days_to_end_of_month()
    pro_rata = (last_day - today) / last_day
    required_amount = 0
    required_payments = await merchant_offers_data_passes_repo.get_merchant_offers_data_passes_requiring_payments(
        merchant_offer_id=merchant_offer_id
    )
    for required_payment in required_payments:
        data_pass = await data_passes_repo.get_data_pass(
            data_pass_id=required_payment.data_pass_id
        )
        if data_pass.status == "active":
            required_amount += int(
                data_pass.price * app_config.NETWORK_PRICE_FACTOR * pro_rata
            )

    balance = await merchant_balances_repo.get_merchant_balance_amount(
        merchant_id=merchant_id
    )

    if balance.amount > required_amount:
        await merchant_balances_repo.create_merchant_balance(
            new_merchant_balance=MerchantBalanceNew(
                merchant_id=merchant_id,
                amount=required_amount,
                balance_type="debit",
                transaction_identifier=merchant_offer_id,
            )
        )
        for required_payment in required_payments:
            await merchant_offers_data_passes_repo.set_merchant_offer_data_pass_validity(
                merchant_offer_id=merchant_offer_id
            )

        return required_amount
    else:
        return -1


def days_to_end_of_month():
    now = datetime.now()
    next_month = now.replace(day=28) + relativedelta(days=4)
    last_day = next_month - relativedelta(days=next_month.day)
    return (now.day, last_day.day)
