from typing import List

import jinja2
from app.apis.utils.notify import Notify
from app.core.global_config import config as app_config
from app.db.repositories.merchants import MerchantsRepository
from app.models.merchant import MerchantEmailView

BATCH_SIZE = 50
MERCHANT_WELCOME_ROOT_LINK = app_config.APPLICATION_ROOT + "/merchant/verify-email"
MERCHANT_WELCOME_TEMPLATE = "datapassport-welcome"

template_loader = jinja2.FileSystemLoader(searchpath="/app/templates")
template_env = jinja2.Environment(loader=template_loader)


async def send_merchant_welcome_email(merchants_repo: MerchantsRepository):
    merchants = await merchants_repo.get_merchants_email_list()

    for i in (0, len(merchants), BATCH_SIZE):
        merchants_to_email = merchants[i : i + BATCH_SIZE]  # noqa: E203
        if len(merchants_to_email) > 0:
            do_send_merchant_welcome_email(merchants_to_email)
            await _flag_merchant_welcome_email_sent(merchants_to_email, merchants_repo)

    notify_marketing(merchants)


def do_send_merchant_welcome_email(merchants: List[MerchantEmailView]):
    destinations = [
        merchant.email for merchant in merchants
    ]
    variables = {
        "verificationLink": "",
        "appName": app_config.APPLICATION_NAME,
        "appLogo": app_config.APPLICATION_LOGO,
        "issuer": app_config.DATA_PASSPORT_ISSUER,
    }
    Notify().send_email(destinations, 'welcome', variables)

async def _flag_merchant_welcome_email_sent(
    merchants: List[MerchantEmailView], merchants_repo: MerchantsRepository
):
    for merchant in merchants:
        await merchants_repo.update_welcome_email_sent(merchant_id=merchant.id)


def notify_marketing(merchants):
    for merchant in merchants:
        if app_config.NOTIFY_MARKETING_EMAIL is not None:
            Notify.send_email(app_config.NOTIFY_MARKETING_EMAIL, 'marketing-merchant-created', merchant.dict())


def notify_support():
    template = template_env.get_template("dataswift-support.html")
    output = template.render({})
    if app_config.NOTIFY_SUPPORT_EMAIL is not None:
        Notify.send_email(app_config.NOTIFY_SUPPORT_EMAIL, 'marketing-merchant-created', merchant.dict())
        # send_email_to_support(
        #     output,
        #     "New Merchant Offer",
        # )
