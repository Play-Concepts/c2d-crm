from typing import Dict

from app.apis.crm.mainmod import main_func
from fastapi import APIRouter


router = APIRouter()


@router.get("/crm/{num}", tags=["crm"])
async def view_b(num: int) -> Dict[str, int]:
    return main_func(num)
