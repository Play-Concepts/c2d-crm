import random
from datetime import datetime
from typing import List

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.db.repositories.merchants import MerchantsRepository
from app.models.merchant import MerchantEmailView, MerchantNew, MerchantView
from app.tests.helpers.data_generator import create_new_merchant

pytestmark = pytest.mark.asyncio


NUMBER_OF_TEST_RECORDS = 5


@pytest.fixture(scope="class")
def new_merchants_test_data() -> List[MerchantNew]:
    return [create_new_merchant() for _ in range(NUMBER_OF_TEST_RECORDS)]
