import codecs
import csv
import uuid
from typing import Any, Dict, List

from fastapi import UploadFile

from app.apis.utils.pda_client import dot_to_dict
from app.db.repositories.customers import CustomersRepository
from app.models.core import CreatedCount
from app.models.customer import CustomerNew


async def do_data_file_upload(
    data_pass_id: uuid.UUID,
    data_table: str,
    customers_file: UploadFile,
    customers_repo: CustomersRepository,
) -> CreatedCount:
    created_customers: int = 0
    payload = _construct_payload(customers_file)
    for customer in payload:
        new_customer: CustomerNew = CustomerNew(
            data=customer, data_pass_id=data_pass_id
        )
        await customers_repo.create_customer(
            new_customer=new_customer, data_table=data_table
        )
        created_customers += 1

    return CreatedCount(count=created_customers)


def _construct_payload(customers_file: UploadFile) -> List[Dict[str, Any]]:
    data = []
    lines = csv.reader(codecs.iterdecode(customers_file.file, "utf-8"), delimiter=",")
    header = next(lines)
    for log_line in lines:
        data.append(dot_to_dict(dict(zip(header, log_line))))

    return data
