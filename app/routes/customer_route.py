from typing import Dict

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from app.apis.customer.mainmod import main_func
from app.core.pda_auth import get_current_pda_user

router = APIRouter()


# Authentication
@router.get("/auth/callback", tags=["authentication"])
async def callback(token: str) -> RedirectResponse:
    return RedirectResponse('/#/pages/customer/basic?token={}'.format(token))


@router.get("/customer/{num}", tags=["customer"])
async def view_b(num: int, auth=Depends(get_current_pda_user)) -> Dict[str, int]:
    return main_func(num)
