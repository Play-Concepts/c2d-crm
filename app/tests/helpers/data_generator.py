from faker import Faker
from faker.providers import company, internet, misc

from app.models.merchant import MerchantNew

fake = Faker()
fake.add_provider(company)
fake.add_provider(internet)
fake.add_provider(misc)


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
