import json
import random
import uuid
from datetime import datetime
from typing import List

from faker import Faker
from faker.providers import address, company, internet, misc
from pydantic.types import Json

from app.apis.utils.random import random_hash
from app.models.activity_log import (ActivityLogComponentType,
                                     ActivityLogEventType, ActivityLogNew)
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


def supplier_email() -> str:
    return fake.email()


def create_new_customer() -> CustomerNew:
    return CustomerNew(
        pda_url=fake.hostname(),
        status=CustomerStatusType.new,
        data=_customer_data(),
        data_pass_id=uuid.uuid4(),
        data_hash=random_hash(),
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


def create_valid_data_pass_source_data(user_id: str) -> dict:
    table_name = fake.first_name().lower()
    search_sql = """SELECT id, data, pda_url, status FROM {data_table}
        WHERE data->'person'->'profile'->>'last_name' ilike :last_name
        AND data->'person'->'address'->>'address_line_1' ilike :address
        AND data->'person'->'contact'->>'email' ilike :email AND status='new';
    """
    return {
        "name": table_name + "-" + fake.pystr_format("?????").lower(),
        "description": fake.sentence(),
        "logo_url": fake.image_url(),
        "data_table": table_name,
        "search_sql": search_sql,
        "data_descriptors": {},
        "user_id": user_id,
    }


def create_valid_data_pass_verifier_data() -> dict:
    return {
        "name": fake.first_name().lower() + "-" + fake.pystr_format("?????").lower(),
        "description": fake.sentence(),
        "logo_url": fake.image_url(),
    }


def create_new_data_pass_data(status: str) -> dict:
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
        "expiry_days": 365,
    }


def _activity_log_component() -> List[ActivityLogComponentType]:
    return [ActivityLogComponentType.perk, ActivityLogComponentType.data_pass]


def _activity_log_event() -> List[ActivityLogEventType]:
    return [
        ActivityLogEventType.view_entered,
        ActivityLogEventType.view_exited,
        ActivityLogEventType.liked,
        ActivityLogEventType.unliked,
        ActivityLogEventType.activited,
        ActivityLogEventType.deactivated,
    ]


def create_random_new_activity_log() -> ActivityLogNew:
    return ActivityLogNew(
        component=random.choice(_activity_log_component()),
        component_identifier=uuid.uuid4(),
        event=random.choice(_activity_log_event()),
    )
