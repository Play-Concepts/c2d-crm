from typing import Dict

from app.apis.customer.mainmod import main_func
from fastapi import APIRouter


router = APIRouter()


@router.get("/customer/{num}", tags=["customer"])
async def view_b(num: int) -> Dict[str, int]:
    return main_func(num)
