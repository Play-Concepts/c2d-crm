import uuid
from typing import Union

from fastapi import Response, status

from app.apis.customer import (customer_claim, customer_data_pass,
                               customer_merchant_offer, customer_transaction)
from app.db.repositories.customers import CustomersRepository
from app.db.repositories.customers_log import CustomersLogRepository
from app.db.repositories.data_pass_sources import DataPassSourcesRepository
from app.db.repositories.data_passes import DataPassesRepository
from app.models.core import BooleanResponse, NotFound
from app.models.customer import CustomerBasicView
from app.models.customer_log import CustomerLogNew
from app.models.data_pass import InvalidDataPass
from app.models.data_pass_source import DataPassSourceDescriptor


async def fn_get_customer_basic(
    data_pass_id: uuid.UUID,
    pda_url: str,
    data_passes_repo: DataPassesRepository,
    data_pass_sources_repo: DataPassSourcesRepository,
    customers_repo: CustomersRepository,
    response: Response,
) -> Union[CustomerBasicView, NotFound, InvalidDataPass]:
    is_valid = await data_passes_repo.is_data_pass_valid(data_pass_id=data_pass_id)
    if is_valid:
        data_descriptors: DataPassSourceDescriptor = (
            await data_pass_sources_repo.get_basic_data_pass_source_search_sql(
                data_pass_id=data_pass_id
            )
        )
        customer = await customers_repo.get_customer_basic(
            pda_url=pda_url,
            data_table=data_descriptors.data_table,
        )
        if customer is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return NotFound(message="Customer Not Found")
        return customer
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return InvalidDataPass()


async def fn_check_first_login(
    pda_url: str,
    customers_log_repo: CustomersLogRepository,
) -> BooleanResponse:
    boolean_response = await customers_log_repo.customer_exists(pda_url=pda_url)
    not_exists = boolean_response.value
    event = "signup" if not_exists else "signin"
    await customers_log_repo.log_event(
        customer_log_new=CustomerLogNew(pda_url=pda_url, event=event)
    )
    return boolean_response


fn_search_customers = customer_claim.fn_search_customers
fn_claim_data = customer_claim.fn_claim_data

fn_get_customer_data_passes = customer_data_pass.fn_get_customer_data_passes
fn_customer_activate_data_pass = customer_data_pass.fn_customer_activate_data_pass
fn_customer_get_scan_transactions_count = (
    customer_transaction.fn_customer_get_scan_transactions_count
)

fn_get_customer_offers = customer_merchant_offer.fn_get_customer_offers
fn_get_all_customer_offers = customer_merchant_offer.fn_get_all_customer_offers
fn_like_merchant_offer = customer_merchant_offer.fn_like_merchant_offer
fn_unlike_merchant_offer = customer_merchant_offer.fn_unlike_merchant_offer
fn_get_customer_favourited_offers = (
    customer_merchant_offer.fn_get_customer_favourited_offers
)
