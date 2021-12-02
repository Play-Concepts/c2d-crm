from typing import Optional

from app.apis.utils.notify import Notify
from app.core.global_config import config as app_config
from app.db.repositories.users import UsersRepository
from app.models.user import UserView


async def fn_create_password(
    token: str, password: str, users_repo: UsersRepository
) -> Optional[UserView]:
    updated_user = await users_repo.create_password(token=token, password=password)
    notifier = Notify()
    if updated_user is not None:
        notifier.send_email(updated_user.email, "password-created", {})

        if app_config.NOTIFY_MARKETING_EMAIL is not None:
            notifier.send_email(
                app_config.NOTIFY_MARKETING_EMAIL,
                "marketing-merchant-verified",
                updated_user.to_dict(),
            )

    return updated_user
