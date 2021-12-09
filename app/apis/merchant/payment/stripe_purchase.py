from typing import Union

import stripe
from fastapi import Request, Response, status
from stripe.error import StripeError

from app.core.global_config import config as app_config
from app.db.repositories.merchant_balances import MerchantBalancesRepository
from app.db.repositories.merchant_payments import MerchantPaymentsRepository
from app.db.repositories.merchants import MerchantsRepository
from app.logger import log_instance
from app.models.core import GenericError, NotFound, StringResponse
from app.models.merchant_balance import BalanceType, MerchantBalanceNew
from app.models.merchant_payment import (MerchantPaymentNew,
                                         MerchantPaymentUpdate, PaymentStatus)
from app.models.stripe import PaymentIntent


async def fn_start_payment(
    merchant_email: str,
    payment_intent: PaymentIntent,
    merchants_repo: MerchantsRepository,
    merchant_payments_repo: MerchantPaymentsRepository,
    request: Request,
    response: Response,
) -> Union[NotFound, GenericError, StringResponse]:
    log = log_instance(request)
    merchant = await merchants_repo.get_merchant_by_email(email=merchant_email)
    if merchant is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFound(message="Merchant Not Found")

    try:
        intent = stripe.PaymentIntent.create(
            amount=payment_intent.amount,
            currency=app_config.NETWORK_CURRENCY,
            payment_method_types=["card"],
        )

        await merchant_payments_repo.create_merchant_payment(
            new_merchant_payment=MerchantPaymentNew(
                merchant_id=merchant.id,
                currency=intent["currency"],
                amount=int(intent["amount"]),
                payment_identifier=intent["id"],
                status=PaymentStatus.new,
            )
        )
    except StripeError as e:
        log.info("stripe_error:{}".format(e.message))
        response.status_code = status.HTTP_400_BAD_REQUEST
        return GenericError("Unable to Initiate Payment.")

    return StringResponse(value=intent["client_secret"])


async def fn_payment_callback(
    payment_intent: stripe.Event,
    merchant_payments_repo: MerchantPaymentsRepository,
    merchant_balances_repo: MerchantBalancesRepository,
    log,
) -> StringResponse:
    log.info(payment_intent["type"])
    if payment_intent["type"] == "payment_intent.succeeded":
        payment_data = payment_intent["data"]["object"]
        payment = await merchant_payments_repo.get_merchant_payment_by_identifier(
            payment_identifier=payment_data["id"]
        )
        if payment is None:
            log.info("payment_not_found:{}".format(payment_data["id"]))
        else:
            if (
                payment.amount == payment_data["amount_received"]
                and payment_data["currency"].lower() == app_config.NETWORK_CURRENCY
            ):
                await merchant_payments_repo.update_merchant_payment_status(
                    merchant_payment_update=MerchantPaymentUpdate(
                        id=payment.id,
                        status=PaymentStatus.completed,
                    )
                )
                await merchant_balances_repo.create_merchant_balance(
                    new_merchant_balance=MerchantBalanceNew(
                        merchant_id=payment.merchant_id,
                        amount=payment.amount,
                        balance_type=BalanceType.credit,
                        transaction_identifier=payment.id,
                    )
                )
                log.info("payment_credited:{}".format(payment_data["id"]))
            else:
                log.info(
                    "payment_not_credited:data_mismatch:{}".format(payment_data["id"])
                )

    return StringResponse(value="Success")
