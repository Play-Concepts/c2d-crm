import uuid
from datetime import datetime, timezone
from typing import List, Union

from fastapi import Request, Response, status
from pydantic.types import Json

from app.apis.utils.pda_client import delete_pda_record, write_pda_data
from app.apis.utils.transformer import transform
from app.core.global_config import config as app_config
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.data_pass_sources import DataPassSourcesRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.logger import log_instance
from app.models.core import NotFound
from app.models.customer import CustomerClaimResponse, CustomerView
from app.models.data_pass import InvalidDataPass
from app.models.data_pass_source import DataPassSourceDescriptor


async def fn_search_customers(
    data_pass_id: uuid.UUID,
    search_params: Json,
    data_passes_repo: DataPassesRepository,
    data_pass_sources_repo: DataPassSourcesRepository,
    customers_repo: CustomersRepository,
    *,
    request: Request,
    response: Response,
) -> Union[InvalidDataPass, List[CustomerView]]:
    log = log_instance(request)
    is_valid = await data_passes_repo.is_data_pass_valid(data_pass_id=data_pass_id)
    if is_valid:
        data_descriptors: DataPassSourceDescriptor = (
            await data_pass_sources_repo.get_data_pass_source(data_pass_id=data_pass_id)
        )

        def transform_view(customer_view: CustomerView):
            data_transformer = (
                None
                if (
                    data_descriptors.data_descriptors is None
                    or ("data_transformer" not in data_descriptors.data_descriptors)
                )
                else data_descriptors.data_descriptors["data_transformer"]
            )
            if data_transformer is not None:
                transform(
                    data_transformer, customer_view.data, search_params=search_params
                )

            return customer_view

        customers = await customers_repo.search_customers(
            data_table=data_descriptors.data_table,
            search_sql=data_descriptors.search_sql,
            transformer=transform_view,
            search_params=search_params,
        )
        log.info("customer-search-result-count({})".format(len(customers)))
        return customers

    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return InvalidDataPass()


async def fn_claim_data(
    data_pass_id: uuid.UUID,
    identifier: uuid.UUID,
    pda_url: str,
    token: str,
    data_passes_repo: DataPassesRepository,
    data_pass_sources_repo: DataPassSourcesRepository,
    customers_repo: CustomersRepository,
    response: Response,
) -> Union[CustomerClaimResponse, NotFound, InvalidDataPass]:
    is_valid = await data_passes_repo.is_data_pass_valid(data_pass_id=data_pass_id)
    if is_valid:
        data_descriptors: DataPassSourceDescriptor = (
            await data_pass_sources_repo.get_basic_data_pass_source_descriptors(
                data_pass_id=data_pass_id
            )
        )
        data_to_claim = await customers_repo.data_to_claim(
            data_table=data_descriptors.data_table,
            identifier=identifier,
        )
        if data_to_claim is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return NotFound(message="Could not find the data to claim")

        claimed_timestamp = datetime.now()

        payload = {
            "data": data_to_claim.data,
            "identifier": str(identifier),
            "claimed_timestamp": claimed_timestamp.replace(
                tzinfo=timezone.utc
            ).isoformat(),
        }

        status_code, pda_response = write_pda_data(
            pda_url,
            token,
            app_config.APPLICATION_NAMESPACE,
            str(data_pass_id),
            payload,
        )
        if status_code == status.HTTP_201_CREATED:
            del payload["data"]
            summary_status_code, summary_pda_response = write_pda_data(
                pda_url,
                token,
                app_config.APPLICATION_NAMESPACE,
                "{}/claim-summary".format(str(data_pass_id)),
                payload,
            )
            claimed_data = await customers_repo.claim_data(
                data_table=data_descriptors.data_table,
                identifier=identifier,
                pda_url=pda_url,
                claimed_timestamp=claimed_timestamp,
            )
            if claimed_data is None:
                # remove data from PDA
                delete_pda_record(
                    pda_url,
                    token,
                    pda_response["recordId"],
                )
                if summary_status_code == status.HTTP_201_CREATED:
                    delete_pda_record(
                        pda_url,
                        token,
                        summary_pda_response["recordId"],
                    )
                response.status_code = status.HTTP_400_BAD_REQUEST
                return InvalidDataPass(message="Unable to commit Claim request.")
            else:
                claimed_data.data_table = data_descriptors.data_table
                return claimed_data
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return InvalidDataPass(
                message="Unable to write data to PDA. {}".format(pda_response["cause"])
            )
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return InvalidDataPass()
