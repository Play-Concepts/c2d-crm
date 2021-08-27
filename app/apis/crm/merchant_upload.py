import codecs
import csv

from fastapi import Request, UploadFile
from fastapi_users import FastAPIUsers

from app.apis.utils.random import random_string
from app.core import global_state
from app.db.repositories.merchants import MerchantsRepository
from app.logger import log_instance
from app.models.core import CreatedCount
from app.models.merchant import MerchantNew
from app.models.user import UserCreate


async def do_merchant_file_upload(
    merchants_file: UploadFile,
    merchants_repo: MerchantsRepository,
    *,
    send_email: bool = True,
    request: Request = None,
) -> CreatedCount:
    created_merchants: int = 0
    lines = csv.reader(codecs.iterdecode(merchants_file.file, "utf-8"), delimiter=",")
    _ = next(lines)
    log = None if request is None else log_instance(request)
    for line in lines:
        (
            first_name,
            last_name,
            company_name,
            trade_name,
            address,
            email,
            phone_number,
            logo_url,
            offer_description,
            offer_start_date,
            offer_end_date,
            agreed_to,
            *end,
        ) = line
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
                "end_date": offer_end_date,
            },
            logo_url=logo_url,
            terms_agreed=(agreed_to == "Yes"),
        )

        created_merchant = await merchants_repo.create_merchant(
            new_merchant=new_merchant
        )
        if created_merchant is not None:
            await _create_merchant_signin_account(
                email=new_merchant.email, fastapi_users=global_state.fastapi_users
            )
            created_merchants += 1

            if log is not None:
                log.info("merchant:account-created:{}".format(email.split("@")[0]))

    return CreatedCount(count=created_merchants)


async def _create_merchant_signin_account(email: str, fastapi_users: FastAPIUsers):
    await fastapi_users.create_user(
        UserCreate(
            email=email,
            password=random_string(),
            is_verified=False,
        )
    )
