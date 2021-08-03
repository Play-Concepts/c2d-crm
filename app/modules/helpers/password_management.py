from fastapi import Request, Depends

from app.apis.crm.merchant_email import do_send_merchant_welcome_email
from app.apis.dependencies.database import get_repository, get_database
from app.apis.utils.emailer import send_templated_email

from app.core.global_config import config as app_config
from app.db.repositories.merchants import MerchantsRepository
from app.models.user import UserDB



async def on_after_forgot_password(user: UserDB, token: str, request: Request):
    if user.is_verified is False:
        return await _resend_welcome_email(user.email, request)

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


async def _resend_welcome_email(email: str, request: Request):
    merchants_repo: MerchantsRepository = get_repository(MerchantsRepository)(get_database(request))
    non_verified_merchant = await merchants_repo.get_merchant_by_email(email=email)
    if non_verified_merchant is not None:
        do_send_merchant_welcome_email([non_verified_merchant])
