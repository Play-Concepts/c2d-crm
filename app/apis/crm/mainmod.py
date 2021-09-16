import uuid
from typing import List, Union

from fastapi import BackgroundTasks, Request, Response, UploadFile, status

from app.db.repositories.customers import CustomersRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.db.repositories.merchants import MerchantsRepository
from app.models.core import CreatedCount, NotFound
from app.models.customer import CustomerView

from . import data_pass_mod
from .customer_upload import do_customer_file_upload
from .merchant_email import send_merchant_welcome_email
from .merchant_upload import do_merchant_file_upload


async def fn_list_customers(
    page: int, page_count: int, customers_repo: CustomersRepository
) -> List[CustomerView]:
    limit = page_count
    offset = (page - 1) * page_count
    return await customers_repo.get_customers(offset=offset, limit=limit)


async def fn_get_customer(
    user_id: uuid.UUID, customers_repo: CustomersRepository, response: Response
) -> Union[CustomerView, NotFound]:
    customer = await customers_repo.get_customer(customer_id=user_id)
    if customer is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFound(message="Customer Not Found")
    return customer


async def fn_customer_upload(
    data_pass_id: uuid.UUID,
    data_passes_repo: DataPassesRepository,
    file: UploadFile,
    customers_repo: CustomersRepository,
) -> CreatedCount:
    is_valid = await data_passes_repo.is_data_pass_valid(data_pass_id=data_pass_id)
    return (
        await do_customer_file_upload(data_pass_id, file, customers_repo)
        if is_valid
        else None
    )


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
