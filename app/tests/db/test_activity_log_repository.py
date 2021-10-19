from datetime import datetime
from typing import List

import pytest
from fastapi.applications import FastAPI
from httpx import AsyncClient

from app.db.repositories.activity_log import ActivityLogRepository
from app.models.activity_log import ActivityLogNew, ActivityLogNewResponse
from app.tests.helpers.data_generator import create_random_new_activity_log

pytestmark = pytest.mark.asyncio

NUMBER_OF_TEST_RECORDS = 5


@pytest.fixture(scope="class")
def new_activity_log_test_data() -> List[ActivityLogNew]:
    return [create_random_new_activity_log() for _ in range(NUMBER_OF_TEST_RECORDS)]


class TestActivityLogRepository:
    async def test_log_activity(
        self,
        app: FastAPI,
        client: AsyncClient,
        activity_log_repository: ActivityLogRepository,
        new_activity_log_test_data: List[ActivityLogNew],
    ):
        for test_new_activity_log in new_activity_log_test_data:
            created_activity_log = await activity_log_repository.log_activity(
                activity_log_new=test_new_activity_log
            )

            assert created_activity_log is not None
            assert isinstance(created_activity_log, ActivityLogNewResponse)
            assert created_activity_log.id is not None
            assert isinstance(created_activity_log.created_at, datetime)
