from typing import Dict

from app.apis.customer.mainmod import main_func
from fastapi import APIRouter
from fastapi.responses import RedirectResponse


router = APIRouter()


# Authentication

@router.get("/auth/callback", tags=["authentication"])
async def callback(token: str) -> RedirectResponse:
    return RedirectResponse('/#/pages/ingest?token={}'.format(token))


@router.get("/customer/{num}", tags=["customer"])
async def view_b(num: int) -> Dict[str, int]:
    return main_func(num)
