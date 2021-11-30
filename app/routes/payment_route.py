from typing import Union

import stripe
from fastapi import APIRouter, Body, Depends, Request, Response

from app.apis.dependencies.database import get_repository
from app.apis.merchant.mainmod import fn_start_payment
from app.core import global_state
from app.db.repositories.merchant_payments import MerchantPaymentsRepository
from app.db.repositories.merchants import MerchantsRepository
from app.logger import log_instance
from app.models.core import NotFound, StringResponse
from app.models.stripe import PaymentIntent

router = APIRouter()
router.prefix = "/api/payment"

merchant_user = global_state.fastapi_users.current_user(
    active=True, verified=True, superuser=False
)


@router.post(
    "/start-payment",
    name="payment:start-payment",
    tags=["payment"],
    responses={
        200: {"model": StringResponse},
        404: {"model": NotFound},
    },
)
async def start_payment(
    response: Response,
    payment_intent: PaymentIntent,
    merchants_repo: MerchantsRepository = Depends(get_repository(MerchantsRepository)),
    merchant_payments_repo: MerchantPaymentsRepository = Depends(
        get_repository(MerchantPaymentsRepository)
    ),
    auth=Depends(merchant_user),
) -> Union[NotFound, StringResponse]:
    return await fn_start_payment(
        auth.email, payment_intent, merchants_repo, merchant_payments_repo, response
    )


@router.post(
    "/callback",
    name="payment:callback",
    tags=["payment"],
    response_model=StringResponse,
)
def payment_callback(
    request: Request,
    payment_intent: stripe.Event = Body(...),
) -> StringResponse:
    log = log_instance(request)
    log.info(payment_intent)
    return StringResponse(value="Success")
