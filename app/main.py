from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routes import crm_route, customer_route
from app.core import auth

app = FastAPI(title="c2d CRM", version="0.5.0-20210422")

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(customer_route.router)
app.include_router(crm_route.router)
