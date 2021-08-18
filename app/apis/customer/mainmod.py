import uuid
from datetime import timezone
from typing import List, Union

from fastapi import Response, status

from app.apis.customer import customer_data_pass
from app.apis.utils.pda_client import write_pda_data
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.customers_log import CustomersLogRepository
from app.models.core import BooleanResponse, NotFound
from app.models.customer import (CustomerBasicView, CustomerClaimResponse,
                                 CustomerView)
from app.models.customer_log import CustomerLogNew


async def fn_get_customer_basic(
    pda_url: str, customers_repo: CustomersRepository, response: Response
) -> Union[CustomerBasicView, NotFound]:
    customer = await customers_repo.get_customer_basic(pda_url=pda_url)
    if customer is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFound(message="Customer Not Found")
    return customer


async def fn_search_customers(
    last_name: str, house_number: str, email: str, customers_repo: CustomersRepository
) -> List[CustomerView]:
    return await customers_repo.search_customers(
        last_name=last_name, house_number=house_number, email=email
    )


async def fn_claim_data(
    identifier: uuid.UUID,
    pda_url: str,
    token: str,
    customers_repo: CustomersRepository,
    response: Response,
) -> Union[CustomerClaimResponse, NotFound]:
    claimed_data = await customers_repo.claim_data(
        identifier=identifier, pda_url=pda_url
    )
    if claimed_data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFound(message="Could not find the data to claim")
    data = claimed_data.data
    data["person"]["identifier"] = str(identifier)
    data["person"]["claimed_timestamp"] = claimed_data.claimed_timestamp.replace(
        tzinfo=timezone.utc
    ).isoformat()
    # TODO: remove hardcoding of default pass when multipass is implemented
    write_pda_data(pda_url, token, "elyria", "elyria-resident", claimed_data.data)
    return claimed_data


async def fn_check_first_login(
    pda_url: str,
    customers_log_repo: CustomersLogRepository,
) -> BooleanResponse:
    boolean_response = await customers_log_repo.customer_exists(pda_url=pda_url)
    await customers_log_repo.log_event(
        customer_log_new=CustomerLogNew(pda_url=pda_url, event="signin")
    )
    return boolean_response


fn_get_customer_data_passes = customer_data_pass.fn_get_customer_data_passes
fn_customer_activate_data_pass = customer_data_pass.fn_customer_activate_data_pass
