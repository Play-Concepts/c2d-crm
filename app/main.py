import uuid

import sentry_sdk
import stripe
from fastapi import FastAPI, Request
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.core import tasks
from app.core.global_config import config as app_config
from app.logger import setup_logging
from app.modules import custom_module, users_module
from app.routes import root_route

sentry_sdk.init(dsn=app_config.SENTRY_DSN)

stripe.api_key = app_config.STRIPE_SECRET_KEY

app = FastAPI(
    title="Data Passport API",
    version="1.0.6l-20211215-PAY",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)


# Inject Request Ids
@app.middleware("http")
async def request_middleware(request: Request, call_next):
    request.state.request_id = uuid.uuid4().hex
    request.state.request_ip = request.client.host
    request.state.request_method = request.method
    response = await call_next(request)
    return response


app.add_middleware(SentryAsgiMiddleware)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", tasks.create_start_app_handler(app))
app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

# Delay FastAPI-Users
app.add_event_handler("startup", users_module.mount_users_module(app))
app.add_event_handler("startup", custom_module.mount_custom_module(app))

app.add_event_handler("startup", setup_logging)

# Hello World
app.include_router(root_route.router)
