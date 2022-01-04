from app.apis.customer import (customer_claim, customer_data_pass,
                               customer_merchant_offer, customer_transaction)
from app.db.repositories.customers_log import CustomersLogRepository
from app.models.core import BooleanResponse
from app.models.customer_log import CustomerLogNew


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
