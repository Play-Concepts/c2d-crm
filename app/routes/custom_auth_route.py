from fastapi import APIRouter, Request, Body

from app.apis.auth.mainmod import fn_create_password

router = APIRouter()
router.prefix = "/api"


@router.post("/auth/create-password", tags=["auth"])
async def create_password(token: str = Body(...), password: str = Body(...)):
    return await fn_create_password(token, password)
