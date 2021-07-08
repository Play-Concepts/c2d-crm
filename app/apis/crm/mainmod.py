from typing import List, Union

from .customer_upload import do_customer_file_upload
import uuid

from app.models.customer import CustomerView
from fastapi import UploadFile, Response, status

from app.db.repositories.customers import CustomersRepository
from app.models.core import CreatedCount, NotFound
from .merchant_upload import do_merchant_file_upload


async def fn_list_customers(page: int,
                            page_count: int,
                            customers_repo: CustomersRepository) -> List[CustomerView]:
    limit = page_count
    offset = (page-1) * page_count
    return await customers_repo.get_customers(offset=offset, limit=limit)


async def fn_get_customer(user_id: uuid.UUID,
                          customers_repo: CustomersRepository,
                          response: Response) -> Union[CustomerView, NotFound]:
    customer = await customers_repo.get_customer(customer_id=user_id)
    if customer is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFound(message="Customer Not Found")
    return customer


async def fn_customer_upload(file: UploadFile, customers_repo: CustomersRepository) -> CreatedCount:
    return await do_customer_file_upload(file, customers_repo)


async def fn_merchant_upload(file: UploadFile) -> CreatedCount:
    return do_merchant_file_upload(file)
