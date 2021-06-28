from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routes import crm_route, customer_route
from app.core import auth, pda_auth, tasks

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

app.include_router(auth.router)
app.include_router(pda_auth.router)
app.include_router(customer_route.router)
app.include_router(crm_route.router)
