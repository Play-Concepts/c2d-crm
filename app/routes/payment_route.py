import stripe
from fastapi import APIRouter, Body, Depends, Request

from app.apis.dependencies.database import get_repository
from app.apis.merchant.mainmod import fn_payment_callback
from app.db.repositories.merchant_balances import MerchantBalancesRepository
from app.db.repositories.merchant_payments import MerchantPaymentsRepository
from app.logger import log_instance
from app.models.core import StringResponse

router = APIRouter()
router.prefix = "/api/payment"


@router.post(
    "/callback",
    name="payment:callback",
    tags=["payment"],
    response_model=StringResponse,
)
async def payment_callback(
    request: Request,
    payment_intent: stripe.Event = Body(...),
    merchant_payments_repo: MerchantPaymentsRepository = Depends(
        get_repository(MerchantPaymentsRepository)
    ),
    merchant_balances_repo: MerchantBalancesRepository = Depends(
        get_repository(MerchantBalancesRepository)
    ),
) -> StringResponse:
    log = log_instance(request)
    return await fn_payment_callback(
        payment_intent, merchant_payments_repo, merchant_balances_repo, log
    )
