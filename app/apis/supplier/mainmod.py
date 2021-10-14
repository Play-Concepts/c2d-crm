import uuid
from typing import List, Union

from fastapi import Response, UploadFile, status

from app.db.repositories.customers import CustomersRepository
from app.db.repositories.data_pass_sources import DataPassSourcesRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.models.core import CreatedCount, FileMismatchError, NotFound
from app.models.customer import CustomerView
from app.models.data_pass import ForbiddenDataPass, InvalidDataPass
from app.models.data_pass_source import DataPassSourceDescriptor

from .supplier_data_upload import do_data_file_upload


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


async def fn_data_upload(
    user_id: uuid.UUID,
    data_pass_id: uuid.UUID,
    data_passes_repo: DataPassesRepository,
    data_pass_sources_repo: DataPassSourcesRepository,
    file: UploadFile,
    customers_repo: CustomersRepository,
    response: Response,
) -> Union[CreatedCount, InvalidDataPass, ForbiddenDataPass, FileMismatchError]:
    is_valid = await data_passes_repo.is_data_pass_valid(data_pass_id=data_pass_id)
    if is_valid:
        if file.filename.lower() != "{}.csv".format(str(data_pass_id).lower()):
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return FileMismatchError(message="Wrong file name.")

        data_descriptors: DataPassSourceDescriptor = (
            await data_pass_sources_repo.get_basic_data_pass_source_descriptors(
                data_pass_id=data_pass_id
            )
        )

        if data_descriptors.user_id != user_id:
            response.status_code = status.HTTP_403_FORBIDDEN
            return ForbiddenDataPass()

        data_keys = (
            []
            if (
                data_descriptors.data_descriptors is None
                or "data_keys" not in data_descriptors.data_descriptors
            )
            else data_descriptors.data_descriptors["data_keys"]
        )

        data_headers = (
            []
            if (
                data_descriptors.data_descriptors is None
                or "data_headers" not in data_descriptors.data_descriptors
            )
            else data_descriptors.data_descriptors["data_headers"]
        )

        data_headers = (
            []
            if (
                data_descriptors.data_descriptors is None
                or "data_headers" not in data_descriptors.data_descriptors
            )
            else data_descriptors.data_descriptors["data_headers"]
        )

        data_root_node = (
            ""
            if (
                data_descriptors.data_descriptors is None
                or ("data_root_node" not in data_descriptors.data_descriptors)
            )
            else data_descriptors.data_descriptors["data_root_node"]
        )

        file_upload = await do_data_file_upload(
            data_pass_id,
            data_descriptors.data_table,
            data_keys,
            data_headers,
            data_root_node,
            file,
            customers_repo,
        )
        if file_upload is None:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return FileMismatchError()
        else:
            return file_upload
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return InvalidDataPass()
