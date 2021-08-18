from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.core import tasks
from app.core.global_config import config
from app.modules import custom_module, users_module
from app.routes import root_route

sentry_sdk.init(dsn=config.SENTRY_DSN)

def init_application():
    app = FastAPI(
        title="Data Passport API",
        version="0.6.0-20210730",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

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

    # Hello World
    app.include_router(root_route.router)

    return app


app = init_application()
