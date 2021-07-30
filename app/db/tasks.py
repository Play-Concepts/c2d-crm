import logging
import os

from databases import Database
from fastapi import FastAPI

from app.core.global_config import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def connect_to_db(app: FastAPI) -> None:
    database_url = f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_SERVER}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"
    if os.environ.get("TEST"):
        database_url += "_test"

    database = Database(
        database_url, min_size=2, max_size=10
    )  # these can be configured in config as well
    try:
        await database.connect()
        app.state.db = database
        logger.info("--- DB CONNECTION ESTABLISHED ---")
    except Exception as e:
        logger.warning("--- DB CONNECTION ERROR ---")
        logger.warning(e)
        logger.warning("--- DB CONNECTION ERROR ---")


async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state.db.disconnect()
    except Exception as e:
        logger.warning("--- DB DISCONNECT ERROR ---")
        logger.warning(e)
        logger.warning("--- DB DISCONNECT ERROR ---")
