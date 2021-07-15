from app.apis.utils.emailer import send_templated_email
from app.models.user import UserDB
from fastapi import Request

from app.core.config import config as app_config


def on_after_forgot_password(user: UserDB, token: str, _: Request):
    reset_link = f'{app_config.APPLICATION_ROOT}/merchant/reset-password/{token}?email={user.email}'
    template_data = {
        'email': user.email,
        'resetLink': reset_link
    }
    send_templated_email(
        user.email,
        'datapassport-reset-password',
        template_data
    )


def on_after_reset_password(user: UserDB, _: Request):
    send_templated_email(
        user.email,
        'datapassport-password-updated',
        {}
    )
