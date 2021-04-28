from typing import List, Any


from .uploadmod import do_file_upload
import uuid

from app.models.customer import Customer
from fastapi import UploadFile


def fn_list_customers() -> List[Customer]:
    return [
        Customer(id=uuid.uuid4().__str__(), name='terry'),
        Customer(id=uuid.uuid4().__str__(), name='thanny'),
        Customer(id=uuid.uuid4().__str__(), name='jenny')
    ]


def fn_get_customer(user_id: str) -> Customer:
    return Customer(id=user_id, name='terry')


def fn_upload(file: UploadFile,
              token: str,
              namespace: str,
              data_path: str
              ) -> Any:
    return do_file_upload(file, token, namespace, data_path)
