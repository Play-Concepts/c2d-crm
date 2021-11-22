import stripe

from app.models.core import StringResponse
from app.models.stripe import PaymentIntent


def fn_start_payment(payment_intent: PaymentIntent) -> StringResponse:
    client_secret = stripe.PaymentIntent.create(
        amount=payment_intent.amount,
        currency=payment_intent.currency,
        payment_method_types=["card"],
    )["client_secret"]

    return StringResponse(value=client_secret)
