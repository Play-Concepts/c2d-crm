import csv
import random
import uuid

from faker import Faker
from faker.providers import address, company, internet, misc

fake = Faker()
fake.add_provider(company)
fake.add_provider(internet)
fake.add_provider(misc)
fake.add_provider(address)

file_name = "customers_speedeon.csv"


def datagenerate(records, headers):
    with open(file_name, "wt") as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        for i in range(records):
            Fname = fake.first_name()
            Lname = fake.last_name()

            Zcode = fake.zipcode()
            Z4code = Zcode[:4]

            user_id = "{}.{}".format(Fname, Lname).lower()

            writer.writerow(
                {
                    "person.profile.first_name": Fname,
                    "person.profile.last_name": Lname,
                    "person.address.address_line_1": fake.street_address(),
                    "person.address.city": fake.city(),
                    "person.address.state": fake.state(),
                    "person.address.zip": Zcode,
                    "person.address.zip4": Z4code,
                    "person.identifiers.speedeon_id": uuid.uuid4().hex,
                    "person.identifiers.email_id_1": random.randint(
                        0, 100000000000000000000
                    ),
                    "person.identifiers.email_id_2": random.randint(
                        0, 100000000000000000000
                    ),
                    "person.identifiers.email_id_3": random.randint(
                        0, 100000000000000000000
                    ),
                    "person.identifiers.email_id_4": random.randint(
                        0, 100000000000000000000
                    ),
                    "person.identifiers.email_id_5": random.randint(
                        0, 100000000000000000000
                    ),
                    "person.contact.email_1": "{}@gmail.com".format(user_id),
                    "person.contact.email_2": "{}@yahoo.com".format(user_id),
                    "person.contact.email_3": "{}@hotmail.com".format(user_id),
                    "person.contact.email_4": "{}@gmx.co.uk".format(user_id),
                    "person.contact.email_5": "{}@singaren.net.sg".format(user_id),
                }
            )


if __name__ == "__main__":
    records = 200
    headers = [
        "person.profile.first_name",
        "person.profile.last_name",
        "person.address.address_line_1",
        "person.address.city",
        "person.address.state",
        "person.address.zip",
        "person.address.zip4",
        "person.identifiers.speedeon_id",
        "person.identifiers.email_id_1",
        "person.identifiers.email_id_2",
        "person.identifiers.email_id_3",
        "person.identifiers.email_id_4",
        "person.identifiers.email_id_5",
        "person.contact.email_1",
        "person.contact.email_2",
        "person.contact.email_3",
        "person.contact.email_4",
        "person.contact.email_5",
    ]

    datagenerate(records, headers)
    print("CSV generation complete!")
