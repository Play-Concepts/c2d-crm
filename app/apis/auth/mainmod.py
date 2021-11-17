from typing import Optional

from app.apis.utils.notify import Notify
from app.core.global_config import config as app_config
from app.db.repositories.users import UsersRepository
from app.models.user import UserView


async def fn_create_password(
    token: str, password: str, users_repo: UsersRepository
) -> Optional[UserView]:
    updated_user = await users_repo.create_password(token=token, password=password)
    if updated_user is not None:
        Notify.send(updated_user.email, 'password-created')

        if app_config.NOTIFY_MARKETING_EMAIL is not None:
            Notify.send(app_config.NOTIFY_MARKETING_EMAIL, 'marketing-merchant-active', updated_user)

    return updated_user
