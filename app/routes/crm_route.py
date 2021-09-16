import uuid
from typing import List, Optional, Union

from fastapi import (APIRouter, BackgroundTasks, Depends, File, Request,
                     Response, UploadFile, status)
from starlette.status import HTTP_201_CREATED

from app.apis.crm.mainmod import (fn_create_data_pass_source,
                                  fn_customer_upload, fn_get_customer,
                                  fn_list_customers, fn_merchant_upload)
from app.apis.dependencies.database import get_repository
from app.core import global_state
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.data_pass_sources import DataPassSourcesRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.db.repositories.merchants import MerchantsRepository
from app.models.core import CreatedCount, IDModelMixin, NotFound
from app.models.customer import CustomerView
from app.models.data_pass import InvalidDataPass
from app.models.data_pass_source import DataPassSourceNew

router = APIRouter()
router.prefix = "/api/crm"

crm_user = global_state.fastapi_users.current_user(
    active=True, verified=True, superuser=True
)


@router.get(
    "/customers",
    name="crm:list_customers",
    tags=["crm"],
    response_model=List[CustomerView],
    deprecated=True,
)
async def list_customers(
    page: Optional[int] = 1,
    page_count: Optional[int] = 20,
    customers_repository: CustomersRepository = Depends(
        get_repository(CustomersRepository)
    ),
    auth=Depends(crm_user),
) -> List[CustomerView]:
    return await fn_list_customers(page, page_count, customers_repository)


@router.get(
    "/customers/{customer_id}",
    name="crm:get_customer",
    tags=["crm"],
    response_model=CustomerView,
    responses={404: {"model": NotFound}},
    deprecated=True,
)
async def get_customer(
    customer_id: uuid.UUID,
    response: Response,
    customers_repo: CustomersRepository = Depends(get_repository(CustomersRepository)),
    auth=Depends(crm_user),
) -> Union[CustomerView, NotFound]:
    return await fn_get_customer(customer_id, customers_repo, response)


@router.post(
    "/customers/upload",
    name="crm:upload_customers",
    tags=["crm"],
    status_code=HTTP_201_CREATED,
    responses={201: {"model": CreatedCount}, 400: {"model": InvalidDataPass}},
    deprecated=True,
)
async def upload_customers(
    response: Response,
    data_pass_id: uuid.UUID,
    data_passes_repo: DataPassesRepository = Depends(
        get_repository(DataPassesRepository)
    ),
    customers_file: UploadFile = File(...),
    customers_repo: CustomersRepository = Depends(get_repository(CustomersRepository)),
    auth=Depends(crm_user),
) -> Union[CreatedCount, InvalidDataPass]:
    upload_count = await fn_customer_upload(
        data_pass_id, data_passes_repo, customers_file, customers_repo
    )
    if upload_count is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return InvalidDataPass()

    return upload_count


@router.post(
    "/merchants/upload",
    name="crm:upload_merchants",
    response_model=CreatedCount,
    tags=["crm"],
    status_code=HTTP_201_CREATED,
)
async def upload_merchants(
    request: Request,
    background_tasks: BackgroundTasks,
    merchants_file: UploadFile = File(...),
    merchants_repo: MerchantsRepository = Depends(get_repository(MerchantsRepository)),
    auth=Depends(crm_user),
) -> CreatedCount:
    return await fn_merchant_upload(
        merchants_file, merchants_repo, background_tasks, request
    )


@router.get(
    "/data-sources",
    name="crm:list_data_sources",
    tags=["crm"],
    response_model=List[CustomerView],
)
async def list_data_sources(
    auth=Depends(crm_user),
):
    return True


@router.post(
    "/data-sources",
    name="crm:create_data_source",
    tags=["crm"],
    response_model=IDModelMixin,
)
async def create_data_source(
    data_pass_source_new: DataPassSourceNew,
    data_pass_sources_repo: DataPassSourcesRepository = Depends(
        get_repository(DataPassSourcesRepository)
    ),
    auth=Depends(crm_user),
) -> IDModelMixin:
    return await fn_create_data_pass_source(
        data_pass_source_new, data_pass_sources_repo
    )


@router.get(
    "/data-sources/{data_source_id}",
    name="crm:get_data_source",
    tags=["crm"],
    response_model=List[CustomerView],
)
async def get_data_source(
    auth=Depends(crm_user),
):
    return True
