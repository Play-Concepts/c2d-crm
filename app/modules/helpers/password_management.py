from app.models.user import UserDB
from fastapi import Request


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print("here")
    print(f"User {user.id} has forgot their password. Reset token: {token}")


def on_after_reset_password(user: UserDB, request: Request):
    print(f"User {user.id} has reset their password.")
