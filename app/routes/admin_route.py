from typing import Dict, List

from app.apis.admin.mainmod import fn_get_user, fn_list_users, User
from fastapi import APIRouter, Depends
from app.core.auth import get_current_user


router = APIRouter()


@router.get("/admin/users", tags=["admin"])
async def list_users(auth=Depends(get_current_user)) -> List[User]:
    return fn_list_users()


@router.get("/admin/users/{user_id}", tags=["admin"])
async def get_user(user_id: str, auth=Depends(get_current_user)) -> User:
    return fn_get_user(user_id)
