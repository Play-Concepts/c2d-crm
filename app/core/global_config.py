import os
from distutils.util import strtobool
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
    APPLICATION_NAMESPACE: Optional[str] = os.environ.get("APPLICATION_NAMESPACE", "")
    APPLICATION_ROOT: Optional[str] = os.environ.get(
        "APPLICATION_ROOT", "http://localhost:3000"
    )
    APPLICATION_NAME: Optional[str] = os.environ.get(
        "APPLICATION_NAME", "sample-datapassport-application"
    )
    APPLICATION_LOGO: Optional[str] = os.environ.get("APPLICATION_LOGO", "")
    SENTRY_DSN: Optional[str] = os.environ.get("SENTRY_DSN", "")

    MAILER_FROM: Optional[str] = os.environ.get("MAILER_FROM", "root@localhost")
    NOTIFY_API: Optional[str] = os.environ.get(
        "NOTIFY_API", "https://one.dataswift.io/notify"
    )
    NOTIFY_TOKEN: Optional[str] = os.environ.get("NOTIFY_TOKEN", "")

    DATA_PASSPORT_ISSUER: Optional[str] = os.environ.get(
        "DATA_PASSPORT_ISSUER", "Sample DP Issuer"
    )
    IP_LOGGING: bool = strtobool(os.environ.get("IP_LOGGING", "False"))

    NOTIFY_MARKETING_EMAIL: Optional[str] = os.environ.get(
        "NOTIFY_MARKETING_EMAIL", None
    )

    NOTIFY_SUPPORT_EMAIL: Optional[str] = os.environ.get("NOTIFY_SUPPORT_EMAIL", None)

    BUCKET_MEDIA: Optional[str] = os.environ.get("BUCKET_MEDIA", None)
    BUCKET_MEDIA_URL: Optional[str] = os.environ.get("BUCKET_MEDIA_URL", None)
    BUCKET_PRIVATE: Optional[str] = os.environ.get("BUCKET_PRIVATE", None)

    STRIPE_SECRET_KEY: Optional[str] = os.environ.get("STRIPE_SECRET_KEY", None)

    # Transient: to be removed when MULTI-TENANCY comes in play
    NETWORK_CURRENCY: str = os.environ.get("NETWORK_CURRENCY", "myr")
    NETWORK_PRICE_FACTOR: int = int(os.environ.get("NETWORK_PRICE_FACTOR", "100"))
    NETWORK_TRANSACTION_COST: int = int(
        os.environ.get("NETWORK_TRANSACTION_COST", "30")
    )

    # Transient
    CHECK_BALANCE: bool = strtobool(os.environ.get("CHECK_BALANCE", "False"))


config = GlobalConfig()
# print(config.__repr__())
