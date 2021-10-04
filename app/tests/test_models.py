from typing import Optional

from app.models.core import IDModelMixin
from app.models.customer import CustomerView


class TestActivatedDataPass:
    activated_data_pass: IDModelMixin


class TestCustomer:
    customer: CustomerView


class TestDataPass:
    data_pass_id: IDModelMixin


class TestDataPassVerifier:
    data_pass_verifier: IDModelMixin


class TestDataTable:
    data_table: str
    search_sql: Optional[str]
