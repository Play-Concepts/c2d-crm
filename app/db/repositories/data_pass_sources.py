import json
import uuid
from typing import Optional

from app.db.repositories.base import BaseRepository
from app.models.core import IDModelMixin
from app.models.data_pass_source import (DataPassSourceDescriptor,
                                         DataPassSourceNew)

NEW_DATA_PASS_SOURCE_SQL = """
    INSERT INTO data_pass_sources(name, description, logo_url, data_table, search_sql, data_descriptors, user_id)
    VALUES(:name, :description, :logo_url, :data_table, :search_sql, :data_descriptors, :user_id)
    RETURNING id
"""

NEW_DATA_PASS_SOURCE_TABLE_SQL_PROC = [
    """
    CREATE TABLE {data_table} (
        id uuid DEFAULT uuid_generate_v4() NOT NULL,
        data json NOT NULL,
        data_hash character varying NOT NULL,
        status claim_status_type DEFAULT 'new'::claim_status_type NOT NULL,
        pda_url character varying(255),
        claimed_timestamp timestamp without time zone,
        created_at timestamp without time zone DEFAULT now() NOT NULL,
        updated_at timestamp without time zone
    );
""",
    """
    ALTER TABLE ONLY {data_table} ADD CONSTRAINT {data_table}_pkey PRIMARY KEY (id);
""",
    """
    CREATE UNIQUE INDEX idx_{data_table}_data_hash ON {data_table} USING btree (data_hash);
""",
    """
    CREATE UNIQUE INDEX idx_{data_table}_pda_url ON {data_table} USING btree (pda_url);
""",
]

GET_DATA_PASS_SOURCE_DESCRIPTORS_SQL = """
    SELECT data_table, null as search_sql, data_descriptors FROM data_pass_sources
    WHERE id in (SELECT data_pass_source_id FROM data_passes WHERE id = :data_pass_id)
"""

GET_DATA_PASS_SOURCE_SEARCH_SQL = """
    SELECT data_table, search_sql, null AS data_descriptors FROM data_pass_sources
    WHERE id in (SELECT data_pass_source_id FROM data_passes WHERE id = :data_pass_id)
"""


class DataPassSourcesRepository(BaseRepository):
    async def create_data_pass_source(
        self, *, data_pass_source_new: DataPassSourceNew
    ) -> IDModelMixin:
        query_values = data_pass_source_new.dict()
        query_values["data_descriptors"] = json.dumps(
            data_pass_source_new.data_descriptors
        )
        data_pass_source = await self.db.fetch_one(
            query=NEW_DATA_PASS_SOURCE_SQL, values=query_values
        )
        return IDModelMixin(**data_pass_source)

    async def create_data_pass_source_table(self, *, data_table: str):
        resp = None
        for statement in NEW_DATA_PASS_SOURCE_TABLE_SQL_PROC:
            resp = await self.db.execute(
                query=statement.format(data_table=data_table),
            )
        return resp

    async def get_basic_data_pass_source_descriptors(
        self, *, data_pass_id: uuid.UUID
    ) -> Optional[DataPassSourceDescriptor]:
        query_values = {"data_pass_id": data_pass_id}
        data_pass_source_descriptor = await self.db.fetch_one(
            query=GET_DATA_PASS_SOURCE_DESCRIPTORS_SQL, values=query_values
        )
        return (
            None
            if data_pass_source_descriptor is None
            else DataPassSourceDescriptor(**data_pass_source_descriptor)
        )

    async def get_basic_data_pass_source_search_sql(
        self, *, data_pass_id: uuid.UUID
    ) -> Optional[DataPassSourceDescriptor]:
        query_values = {"data_pass_id": data_pass_id}
        data_pass_source_descriptor = await self.db.fetch_one(
            query=GET_DATA_PASS_SOURCE_SEARCH_SQL, values=query_values
        )
        return (
            None
            if data_pass_source_descriptor is None
            else DataPassSourceDescriptor(**data_pass_source_descriptor)
        )
