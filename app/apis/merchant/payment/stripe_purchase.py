from typing import Union

import stripe
from fastapi import Response, status

from app.db.repositories.merchant_payments import MerchantPaymentsRepository
from app.db.repositories.merchants import MerchantsRepository
from app.models.core import NotFound, StringResponse
from app.models.merchant_payment import MerchantPaymentNew
from app.models.stripe import PaymentIntent


async def fn_start_payment(
    merchant_email: str,
    payment_intent: PaymentIntent,
    merchants_repo: MerchantsRepository,
    merchant_payments_repo: MerchantPaymentsRepository,
    response: Response,
) -> Union[NotFound, StringResponse]:
    merchant = await merchants_repo.get_merchant_by_email(email=merchant_email)
    if merchant is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFound(message="Merchant Not Found")

    intent = stripe.PaymentIntent.create(
        amount=payment_intent.amount,
        currency=payment_intent.currency,
        payment_method_types=["card"],
    )
    

    await merchant_payments_repo.create_merchant_payment(
        new_merchant_payment=MerchantPaymentNew(
            merchant_id=merchant.id,
            currency=intent["currency"],
            amount=int(intent["amount"]),
            payment_identifier=intent["id"],
            status="new",
        )
    )

    return StringResponse(value=intent["client_secret"])
