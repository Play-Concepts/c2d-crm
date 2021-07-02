#
# This defines the data model for BOTH Merchant and CRM User.
#
from typing import Optional

from fastapi_users import models


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    password_change_token: Optional[str]


class UserDB(User, models.BaseUserDB):
    password_change_token: str
