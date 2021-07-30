from typing import Callable

from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from app.core import global_state
from app.core.global_config import config
from app.models.user import User, UserCreate, UserDB, UserUpdate
from app.modules.helpers.password_management import (
    on_after_forgot_password,
    on_after_reset_password,
)


def mount_users_module(app: FastAPI) -> Callable:
    async def start_app() -> None:
        secret = config.SECRET_KEY
        auth_backends = []
        jwt_authentication = JWTAuthentication(
            name="datapassword-auth",
            secret=secret,
            lifetime_seconds=3600,
            tokenUrl="auth/jwt/login",
        )
        auth_backends.append(jwt_authentication)

        Base: DeclarativeMeta = declarative_base()

        class UsersTable(Base, SQLAlchemyBaseUserTable):
            __tablename__ = "users"

        users = UsersTable.__table__
        user_db = SQLAlchemyUserDatabase(UserDB, app.state.db, users)

        fastapi_users = FastAPIUsers(
            user_db, auth_backends, User, UserCreate, UserUpdate, UserDB
        )

        app.include_router(
            fastapi_users.get_auth_router(jwt_authentication),
            prefix="/api/auth/jwt",
            tags=["auth"],
        )
        app.include_router(
            fastapi_users.get_reset_password_router(
                secret,
                after_reset_password=on_after_reset_password,
                after_forgot_password=on_after_forgot_password,
            ),
            prefix="/api/auth",
            tags=["auth"],
        )

        global_state.fastapi_users = fastapi_users
        global_state.authenticator = jwt_authentication

    return start_app
