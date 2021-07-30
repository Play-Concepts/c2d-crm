import codecs
import csv
from functools import reduce
from typing import Any, Dict, List

from fastapi import UploadFile

from app.db.repositories.customers import CustomersRepository
from app.models.core import CreatedCount
from app.models.customer import CustomerNew


async def do_customer_file_upload(
    customers_file: UploadFile, customers_repo: CustomersRepository
) -> CreatedCount:
    created_customers: int = 0
    payload = _construct_payload(customers_file)
    for customer in payload:
        new_customer: CustomerNew = CustomerNew(data=customer).init_new()
        await customers_repo.create_customer(new_customer=new_customer)
        created_customers += 1

    return CreatedCount(count=created_customers)


def _construct_payload(customers_file: UploadFile) -> List[Dict[str, Any]]:
    data = []
    lines = csv.reader(codecs.iterdecode(customers_file.file, "utf-8"), delimiter=",")
    header = next(lines)
    for log_line in lines:
        data.append(_dot_to_dict(dict(zip(header, log_line))))

    return data


def _dot_to_dict(a):
    output = {}
    for key, value in a.items():
        pre_path, *data_type = key.split("/")
        path = pre_path.split(".")
        val = value
        if len(data_type) == 1:
            if data_type[0] == "int":
                val = int(value)
            if data_type[0] == "float":
                val = float(value)
        target = reduce(lambda d, k: d.setdefault(k, {}), path[:-1], output)
        target[path[-1]] = val

    return output
