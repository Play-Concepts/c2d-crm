import json
from typing import List

from app.apis.utils.emailer import send_bulk_templated_email
from app.core.config import config as app_config
from app.db.repositories.merchants import MerchantsRepository
from app.models.merchant import MerchantEmailView

BATCH_SIZE = 50
MERCHANT_WELCOME_ROOT_LINK = app_config.APPLICATION_ROOT + '/merchant/verify-email'
MERCHANT_WELCOME_TEMPLATE = 'datapassport-welcome'


async def send_merchant_welcome_email(merchants_repo: MerchantsRepository):
    merchants = await merchants_repo.get_merchants_email_list()

    for i in (0, len(merchants), BATCH_SIZE):
        merchants_to_email = merchants[i:i+BATCH_SIZE]
        if len(merchants_to_email) > 0:
            _do_send_merchant_welcome_email(merchants_to_email)
            await _flag_merchant_welcome_email_sent(merchants_to_email, merchants_repo)


def _do_send_merchant_welcome_email(merchants:List[MerchantEmailView]):
    destinations = [_create_merchant_email_destination(merchant) for merchant in merchants]
    # TODO extract to ENV file
    default_data = {
        "verificationLink": "",
        "appName": app_config.APPLICATION_NAME,
        "appLogo": app_config.APPLICATION_LOGO,
    }
    send_bulk_templated_email(destinations,
                              MERCHANT_WELCOME_TEMPLATE,
                              json.dumps(default_data))


def _create_merchant_email_destination(merchant: MerchantEmailView):
    # TODO proper callback link
    template_data = {
        'verificationLink': '{}/{}?email={}'.format(MERCHANT_WELCOME_ROOT_LINK, merchant.password_change_token, merchant.email),
    }
    return {
        'Destination': {
            'ToAddresses': [
                merchant.email,
            ],
        },
        'ReplacementTemplateData': json.dumps(template_data)
    }


async def _flag_merchant_welcome_email_sent(merchants:List[MerchantEmailView], merchants_repo: MerchantsRepository):
    for merchant in merchants:
        await merchants_repo.update_welcome_email_sent(merchant_id=merchant.id)