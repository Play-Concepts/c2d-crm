from typing import Callable

from fastapi import FastAPI


def mount_custom_module(app: FastAPI) -> Callable:
    async def start_app() -> None:
        from app.routes import (
            crm_route,
            custom_auth_route,
            customer_route,
            merchant_route,
        )

        app.include_router(customer_route.router)
        app.include_router(crm_route.router)
        app.include_router(custom_auth_route.router)
        app.include_router(merchant_route.router)

    return start_app
