import os
from typing import Optional

from pydantic import BaseSettings


class GlobalConfig(BaseSettings):
    """Global configurations."""

    # This variable will be loaded from the .env file. However, if there is a
    # shell environment variable having the same name, that will take precedence.

    # the class Field is necessary while defining the global variables
    ENV_STATE: Optional[str] = os.environ.get("ENV_STATE", "dev")

    SECRET_KEY: Optional[str] = os.environ.get("SECRET_KEY", None)
    POSTGRES_USER: Optional[str] = os.environ.get("POSTGRES_USER", None)
    POSTGRES_PASSWORD: Optional[str] = os.environ.get("POSTGRES_PASSWORD", None)
    POSTGRES_SERVER: Optional[str] = os.environ.get("POSTGRES_SERVER", None)
    POSTGRES_PORT: Optional[str] = os.environ.get("POSTGRES_PORT", None)
    POSTGRES_DB: Optional[str] = os.environ.get("POSTGRES_DB", None)
    APPLICATION_ID: Optional[str] = os.environ.get("APPLICATION_ID", "")
    APPLICATION_ROOT: Optional[str] = os.environ.get(
        "APPLICATION_ROOT", "http://localhost:3000"
    )
    APPLICATION_NAME: Optional[str] = os.environ.get(
        "APPLICATION_NAME", "sample-datapassport-application"
    )
    APPLICATION_LOGO: Optional[str] = os.environ.get("APPLICATION_LOGO", "")
    SENTRY_DSN: Optional[str] = os.environ.get("SENTRY_DSN", "")

    MAILER_FROM: Optional[str] = os.environ.get("MAILER_FROM", "root@localhost")
    DATA_PASSPORT_ISSUER: Optional[str] = os.environ.get(
        "DATA_PASSPORT_ISSUER", "Sample DP Issuer"
    )
    IP_LOGGING: Optional[str] = os.environ.get("IP_LOGGING", False)


config = GlobalConfig()
# print(config.__repr__())
