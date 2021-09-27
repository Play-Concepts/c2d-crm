import uuid
from typing import Union

from fastapi import APIRouter, Depends, File, Response, UploadFile
from starlette.status import HTTP_201_CREATED

from app.apis.dependencies.database import get_repository
from app.apis.supplier.mainmod import fn_data_upload
from app.core.auth import current_supplier
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.data_pass_sources import DataPassSourcesRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.models.core import CreatedCount, FileMismatchError
from app.models.data_pass import ForbiddenDataPass, InvalidDataPass

router = APIRouter()
router.prefix = "/api/supplier"


@router.post(
    "/data/{data_pass_id}/upload",
    name="supplier:upload_data",
    tags=["suppliers"],
    status_code=HTTP_201_CREATED,
    responses={
        201: {"model": CreatedCount},
        400: {"model": InvalidDataPass},
        403: {"model": ForbiddenDataPass},
        422: {"model": FileMismatchError},
    },
)
async def upload_data(
    response: Response,
    data_pass_id: uuid.UUID,
    data_passes_repo: DataPassesRepository = Depends(
        get_repository(DataPassesRepository)
    ),
    data_pass_sources_repo: DataPassSourcesRepository = Depends(
        get_repository(DataPassSourcesRepository)
    ),
    customers_file: UploadFile = File(...),
    customers_repo: CustomersRepository = Depends(get_repository(CustomersRepository)),
    auth=Depends(current_supplier),
) -> Union[CreatedCount, InvalidDataPass, ForbiddenDataPass, FileMismatchError]:
    return await fn_data_upload(
        auth.id,
        data_pass_id,
        data_passes_repo,
        data_pass_sources_repo,
        customers_file,
        customers_repo,
        response,
    )
