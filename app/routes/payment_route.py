from fastapi import APIRouter, Depends

from app.apis.merchant.mainmod import fn_start_payment
from app.core import global_state
from app.models.core import StringResponse
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
    response_model=StringResponse,
)
def get_products(
    payment_intent: PaymentIntent,
    auth=Depends(merchant_user),
) -> StringResponse:
    return fn_start_payment(payment_intent)
