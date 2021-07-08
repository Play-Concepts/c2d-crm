from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core import tasks
from . import users_module
from . import custom_module

app = FastAPI(title="c2d CRM", version="0.5.0-20210517")

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
