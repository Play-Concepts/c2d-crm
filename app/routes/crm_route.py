from typing import List, Optional

from fastapi import (APIRouter, BackgroundTasks, Depends, File, Request,
                     UploadFile)
from starlette.status import HTTP_201_CREATED

from app.apis.crm.mainmod import fn_create_data_pass_source, fn_merchant_upload
from app.apis.dependencies.database import get_repository
from app.apis.utils.random import random_string
from app.core import global_state
from app.db.repositories.data_pass_sources import DataPassSourcesRepository
from app.db.repositories.merchants import MerchantsRepository
from app.models.core import CreatedCount, IDModelMixin
from app.models.customer import CustomerView
from app.models.data_pass_source import (DataPassSourceNew,
                                         DataPassSourceRequest)
from app.models.user import UserCreate

router = APIRouter()
router.prefix = "/api/crm"

crm_user = global_state.fastapi_users.current_user(
    active=True, verified=True, superuser=True
)


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
    email: Optional[str],
    data_pass_source_request: DataPassSourceRequest,
    data_pass_sources_repo: DataPassSourcesRepository = Depends(
        get_repository(DataPassSourcesRepository)
    ),
    auth=Depends(crm_user),
) -> IDModelMixin:
    user_id = None
    if email is not None:
        fastapi_users = global_state.fastapi_users
        user = await fastapi_users.create_user(
            UserCreate(
                email=email,
                password=random_string(),
                is_verified=True,
                is_supplier=True,
            )
        )
        user_id = user.id

    data = data_pass_source_request.dict()
    data["user_id"] = user_id
    return await fn_create_data_pass_source(
        DataPassSourceNew(**data), data_pass_sources_repo
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
