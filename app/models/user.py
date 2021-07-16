#
# This defines the data model for BOTH Merchant and CRM User.
#
from fastapi_users import models

from app.models.core import IDModelMixin


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


class UserView(IDModelMixin):
    email: str
