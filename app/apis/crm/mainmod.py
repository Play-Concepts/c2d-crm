from fastapi import BackgroundTasks, Request, UploadFile

from app.db.repositories.merchants import MerchantsRepository
from app.models.core import CreatedCount

from . import data_pass_mod
from .merchant_email import send_merchant_welcome_email
from .merchant_upload import do_merchant_file_upload


async def fn_merchant_upload(
    file: UploadFile,
    merchant_repo: MerchantsRepository,
    background_tasks: BackgroundTasks = None,
    request: Request = None,
) -> CreatedCount:
    created_count = await do_merchant_file_upload(file, merchant_repo, request=request)
    if background_tasks is not None:
        background_tasks.add_task(send_merchant_welcome_email, merchant_repo)
    return created_count


fn_create_data_pass_source = data_pass_mod.fn_create_data_pass_source
