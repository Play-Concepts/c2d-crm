import sqlalchemy as sa
from fastapi_users.db import SQLAlchemyBaseUserTable
from fastapi_users.db.base import UserDatabaseDependency
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from app.core import global_state

Base: DeclarativeMeta = declarative_base()


class UsersTable(Base, SQLAlchemyBaseUserTable):
    __tablename__ = "users"
    is_supplier = sa.Column(sa.Boolean, nullable=False, server_default=sa.text("false"))


users = UsersTable.__table__


def get_user_db():
    yield SQLAlchemyUserDatabase(UserDatabaseDependency, global_state.db, users)
