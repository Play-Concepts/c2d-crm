from fastapi import APIRouter, Body, Depends, Response, status

from app.apis.auth.mainmod import fn_create_password
from app.apis.dependencies.database import get_repository
from app.core import global_state
from app.db.repositories.users import UsersRepository
from app.models.core import InvalidToken

router = APIRouter()
router.prefix = "/api"

fastapi_users = global_state.fastapi_users
authenticator = global_state.authenticator


@router.post("/auth/create-password", name="auth:create-password", tags=["auth"])
async def create_password(
    response: Response,
    token: str = Body(...),
    password: str = Body(...),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
):
    updated_user = await fn_create_password(token, password, users_repo)
    if updated_user is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return InvalidToken(message="Invalid Password Token")
    else:
        user = await fastapi_users.get_user(updated_user.email)
        return await authenticator.get_login_response(user, response)
