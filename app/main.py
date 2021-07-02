from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.apis.dependencies.database import get_database
from app.core.config import config
from app.models.user import User, UserCreate, UserUpdate, UserDB
from app.routes import crm_route, customer_route
from app.core import auth, pda_auth, tasks

from fastapi import Depends

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


from fastapi_users.authentication import JWTAuthentication

SECRET = config.SECRET_KEY
auth_backends = []
jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600, tokenUrl="auth/jwt/login")
auth_backends.append(jwt_authentication)


from fastapi_users import FastAPIUsers
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class UserTable(Base, SQLAlchemyBaseUserTable):
    pass


users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, Depends(get_database), users)

fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

app.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(SECRET),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
    tags=["users"],
)
app.include_router(
    fastapi_users.get_verify_router(SECRET),
    prefix="/auth",
    tags=["auth"],
)

