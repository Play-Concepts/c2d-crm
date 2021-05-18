from typing import Dict

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.apis.customer.mainmod import main_func

router = APIRouter()


# Authentication

@router.get("/auth/callback", tags=["authentication"])
async def callback(token: str) -> RedirectResponse:
    return RedirectResponse('/#/pages/customer/basic?token={}'.format(token))


@router.get("/customer/{num}", tags=["customer"])
async def view_b(num: int) -> Dict[str, int]:
    return main_func(num)
