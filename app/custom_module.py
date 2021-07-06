from typing import Callable
from fastapi import FastAPI


def mount_custom_module(app: FastAPI) -> Callable:
    async def start_app() -> None:
        from app.routes import crm_route, customer_route
        app.include_router(customer_route.router)
        app.include_router(crm_route.router)

    return start_app
