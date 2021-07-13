import csv
import codecs

from app import global_state
from app.db.repositories.merchants import MerchantsRepository
from app.models.core import CreatedCount

from fastapi import UploadFile
from fastapi_users import FastAPIUsers

from app.models.merchant import MerchantNew
from app.models.user import UserCreate

import secrets
import string


async def do_merchant_file_upload(merchants_file: UploadFile, merchants_repo:MerchantsRepository) -> CreatedCount:
    created_merchants: int = 0
    lines = csv.reader(codecs.iterdecode(merchants_file.file, 'utf-8'), delimiter=',')
    header = next(lines)
    for line in lines:
        first_name, last_name, company_name, trade_name, address, email, phone_number, offer_description, \
            offer_start_date, offer_end_date, logo_url, *end = line
        new_merchant: MerchantNew = MerchantNew(
            first_name=first_name,
            last_name=last_name,
            company_name=company_name,
            trade_name=trade_name,
            address=address,
            email=email,
            phone_number=phone_number,
            offer={
                "description": offer_description,
                "start_date": offer_start_date,
                "end_date": offer_end_date
            },
            logo_url=logo_url,
        )
        created_merchant = await merchants_repo.create_merchant(new_merchant=new_merchant)
        if created_merchant is not None:
            await _create_merchant_signin_account(email=new_merchant.email, fastapi_users=global_state.fastapi_users)
            created_merchants += 1

    return CreatedCount(count=created_merchants)


async def _create_merchant_signin_account(email: str, fastapi_users: FastAPIUsers):
    await fastapi_users.create_user(UserCreate(
        email=email,
        password=_random_password(),
    ))


def _random_password() -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(20))
