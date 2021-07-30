from typing import Optional

from app.apis.utils.emailer import send_templated_email
from app.db.repositories.users import UsersRepository
from app.models.user import UserView


async def fn_create_password(
    token: str, password: str, users_repo: UsersRepository
) -> Optional[UserView]:
    updated_user = await users_repo.create_password(token=token, password=password)
    if updated_user is not None:
        send_templated_email(updated_user.email, "datapassport-password-created", {})

    return updated_user
