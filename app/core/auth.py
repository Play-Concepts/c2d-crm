from fastapi import Depends, HTTPException, status

from app.core import global_state

active_user = global_state.fastapi_users.current_user(
    active=True, verified=True, superuser=False
)


async def current_supplier(user=Depends(active_user)):
    if user.is_supplier is False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user
