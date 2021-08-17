from typing import Optional

from app.apis.utils.emailer import send_templated_email, send_notification_email_to_marketing
from app.db.repositories.users import UsersRepository
from app.models.user import UserView
from app.core.global_config import config as app_config


async def fn_create_password(
    token: str, password: str, users_repo: UsersRepository
) -> Optional[UserView]:
    updated_user = await users_repo.create_password(token=token, password=password)
    if updated_user is not None:
        send_templated_email(updated_user.email, "datapassport-password-created", {})
        if app_config.NOTIFY_MARKETING_EMAIL is not None:
            send_notification_email_to_marketing(updated_user.email, app_config.NOTIFY_MARKETING_EMAIL)

    return updated_user
