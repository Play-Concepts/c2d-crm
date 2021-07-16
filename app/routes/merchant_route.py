from fastapi import APIRouter, Body, Depends, Request

from app import global_state

router = APIRouter()
router.prefix = "/api"

merchant_user = global_state.fastapi_users.current_user(active=True, verified=True, superuser=True)


@router.post("/merchant/barcode/verify", tags=["merchants"])
async def verify_barcode(request: Request, barcode: str = Body(..., embed=True),
                         auth=Depends(merchant_user)):
    return {
        'barcode': barcode
    }
