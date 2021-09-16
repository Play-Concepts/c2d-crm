import json
import uuid
from datetime import datetime
from typing import List

from faker import Faker
from faker.providers import address, company, internet, misc
from pydantic.types import Json

from app.models.customer import CustomerNew
from app.models.customer import StatusType as CustomerStatusType
from app.models.customer_log import CustomerLogNew
from app.models.merchant import MerchantNew

fake = Faker()
fake.add_provider(company)
fake.add_provider(internet)
fake.add_provider(misc)
fake.add_provider(address)


def create_new_merchant() -> MerchantNew:
    company_name = fake.company()
    return MerchantNew(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        company_name="{} {}".format(company_name, fake.company_suffix()),
        trade_name=company_name,
        address=fake.address(),
        email=fake.company_email(),
        phone_number=fake.phone_number(),
        offer={
            "description": fake.catch_phrase(),
            "start_date": fake.date(),
            "end_date": fake.date(),
        },
        logo_url=fake.image_url(),
        terms_agreed=fake.boolean(chance_of_getting_true=50),
    )


def create_new_customer() -> CustomerNew:
    return CustomerNew(
        pda_url=fake.hostname(),
        status=CustomerStatusType.new,
        data=_customer_data(),
        data_pass_id=uuid.uuid4(),
    )


def _customer_data() -> Json:
    data = {
        "person": {
            "address": {
                "city": fake.city(),
                "address_line_1": fake.street_address(),
            },
            "contact": {
                "email": fake.email(),
            },
            "profile": {
                "last_name": fake.last_name(),
                "first_name": fake.first_name(),
            },
            "identifier": str(uuid.uuid4()),
            "claimed_timestamp": datetime.now().isoformat(),
        }
    }
    return json.dumps(data)


def _customer_status() -> List[CustomerStatusType]:
    return [CustomerStatusType.new, CustomerStatusType.claimed]


def create_new_customer_log() -> CustomerLogNew:
    return CustomerLogNew(
        pda_url=fake.domain_name(),
        event="signup",
    )


def fake_hostname() -> str:
    return fake.hostname()


def create_valid_data_pass_source_data() -> dict:
    return {
        "name": fake.first_name().lower() + "-" + fake.pystr_format("?????").lower(),
        "description": fake.sentence(),
        "logo_url": fake.image_url(),
        "data_table": "",
        "search_sql": "",
        "search_parameters": "",
    }


def create_valid_data_pass_verifier_data() -> dict:
    return {
        "name": fake.first_name().lower() + "-" + fake.pystr_format("?????").lower(),
        "description": fake.sentence(),
        "logo_url": fake.image_url(),
    }


def create_new_data_pass_data(status: str, expiry_date: datetime) -> dict:
    return {
        "name": fake.first_name().lower() + "-" + fake.pystr_format("?????").lower(),
        "title": fake.sentence(),
        "description_for_merchants": fake.sentence(),
        "description_for_customers": fake.sentence(),
        "perks_url_for_merchants": fake.url(),
        "perks_url_for_customers": fake.url(),
        "currency_code": "USD",
        "price": 0,
        "status": status,
        "expiry_date": expiry_date,
    }
