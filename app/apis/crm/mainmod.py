from typing import List, Any

import json
from .uploadmod import do_file_upload
import uuid

from app.models.customer import CustomerView
from fastapi import UploadFile


fake_terry_data = json.dumps({
    "person": {
        "profile": {
            "first_name": "Terry",
            "last_name": "Lee"
        },
        "address": {
            "address_line_1": "2 Playsteds Lane",
            "city": "Cambridge"
        },
        "contact": {
            "email": "terry.lee@hello.world"
        }
    }
})

fake_thanny_data = json.dumps({
    "person": {
        "profile": {
            "first_name": "Thanny",
            "last_name": "Lee"
        },
        "address": {
            "address_line_1": "5 Nomad Close",
            "city": "Melbourne"
        },
        "contact": {
            "email": "thanny.lee@hello.world"
        }
    }
})

fake_jenny_data = json.dumps({
    "person": {
        "profile": {
            "first_name": "Jenny",
            "last_name": "Nyugen"
        },
        "address": {
            "address_line_1": "58 The Bund",
            "city": "Shanghai"
        },
        "contact": {
            "email": "jenny@hello.world"
        }
    }
})


def fn_list_customers() -> List[CustomerView]:
    return [
        CustomerView(id=uuid.UUID("66d3eade-edf5-477a-866e-9f818f7e4a9b"), data=fake_terry_data, pda_url="terryds.hubofallthings.net", status="claimed"),
        CustomerView(id=uuid.UUID("b7039ad3-4dc9-4da2-8583-50d8a7866469"), data=fake_thanny_data, pda_url="", status="new"),
        CustomerView(id=uuid.UUID("fe337452-8749-4b21-92e0-4108bfcd5ca4"), data=fake_jenny_data, pda_url="", status="new"),
    ]


def fn_get_customer(user_id: str) -> CustomerView:
    return CustomerView(id=uuid.UUID(user_id), data=fake_terry_data, pda_url="terryds.hubofallthings.net", status="claimed")


def fn_upload(file: UploadFile) -> Any:
    return do_file_upload(file)
