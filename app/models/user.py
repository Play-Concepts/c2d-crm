#
# This defines the data model for BOTH Merchant and CRM User.
#
from typing import Optional

from fastapi_users import models

from app.models.core import IDModelMixin


class User(models.BaseUser):
    is_supplier: bool


class UserCreate(models.BaseUserCreate):
    is_supplier: Optional[bool] = False


class UserUpdate(User, models.BaseUserUpdate):
    is_supplier: Optional[bool] = False


class UserDB(User, models.BaseUserDB):
    is_supplier: Optional[bool] = False


class UserView(IDModelMixin):
    email: str
