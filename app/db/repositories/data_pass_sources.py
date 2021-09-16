from app.db.repositories.base import BaseRepository
from app.models.core import IDModelMixin
from app.models.data_pass_source import DataPassSourceNew

NEW_DATA_PASS_SOURCE_SQL = """
    INSERT INTO data_pass_sources(name, description, logo_url, data_table, search_sql, search_parameters, user_id)
    VALUES(:name, :description, :logo_url, :data_table, :search_sql, :search_parameters, :user_id)
    RETURNING id
"""

NEW_DATA_PASS_SOURCE_TABLE_SQL_PROC = ["""
    CREATE TABLE {data_table} (
        id uuid DEFAULT uuid_generate_v4() NOT NULL,
        data json NOT NULL,
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
    CREATE UNIQUE INDEX idx_{data_table}_pda_url ON {data_table} USING btree (pda_url);
"""]

class DataPassSourcesRepository(BaseRepository):
    async def create_data_pass_source(
        self, *, data_pass_source_new: DataPassSourceNew
    ) -> IDModelMixin:
        query_values = data_pass_source_new.dict()
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
