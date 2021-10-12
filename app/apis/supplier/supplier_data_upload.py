import codecs
import csv
import uuid
from typing import Any, Dict, List, Optional

from fastapi import UploadFile
from loguru import logger

from app.apis.utils.pda_client import dot_to_dict
from app.db.repositories.customers import CustomersRepository
from app.models.core import CreatedCount
from app.models.customer import CustomerNew


async def do_data_file_upload(
    data_pass_id: uuid.UUID,
    data_table: str,
    data_keys: List[str],
    data_headers: List[str],
    data_root_node: str,
    customers_file: UploadFile,
    customers_repo: CustomersRepository,
) -> Optional[CreatedCount]:
    created_customers: int = 0
    payload = _construct_payload(customers_file, data_headers, data_root_node)
    if payload is None:
        return None

    for customer in payload:
        logger.info(customer)
        new_customer: CustomerNew = CustomerNew(
            data=customer, data_pass_id=data_pass_id
        )
        new_customer.before_save(keys=data_keys)
        customer = await customers_repo.create_customer(
            new_customer=new_customer, data_table=data_table
        )
        created_customers += 1 if customer is not None else 0

    return CreatedCount(count=created_customers)


def _construct_payload(
    customers_file: UploadFile,
    data_headers: List[str],
    root_node: str,
) -> Optional[List[Dict[str, Any]]]:
    data = []
    lines = csv.reader(codecs.iterdecode(customers_file.file, "utf-8"), delimiter=",")
    headers = next(lines)
    if len(data_headers) != 0:
        is_headers_match = _match_headers(headers, data_headers)
        if is_headers_match is False:
            return None

    node_headers = ["{}{}".format(root_node, header) for header in headers]
    for log_line in lines:
        data.append(
            dot_to_dict(
                dict(zip(node_headers, log_line)),
            )
        )

    return data


def _match_headers(headers: List[str], data_headers: List[str]) -> bool:
    headers_cp = headers.copy()
    data_headers_cp = data_headers.copy()
    headers_cp.sort()
    data_headers_cp.sort()
    return headers_cp == data_headers_cp
