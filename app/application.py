import sentry_sdk
from fastapi import FastAPI, Request
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.core import tasks
from app.core.global_config import config
from app.modules import custom_module, users_module
from app.routes import root_route

sentry_sdk.init(dsn=config.SENTRY_DSN)

import uuid

from loguru import logger


# Inject Request Ids
async def request_middleware(request: Request):
    request_id = uuid.uuid4().hex
    logger.bind(request_id=request_id)


application = FastAPI(
    title="Data Passport API",
    version="0.2.7-20210824",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

application.add_middleware(SentryAsgiMiddleware)

# Set all CORS enabled origins
application.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

application.add_event_handler(
    "startup", tasks.create_start_application_handler(application)
)
application.add_event_handler(
    "shutdown", tasks.create_stop_application_handler(application)
)

# Delay FastAPI-Users
application.add_event_handler("startup", users_module.mount_users_module(application))
application.add_event_handler("startup", custom_module.mount_custom_module(application))

# Hello World
application.include_router(root_route.router)
