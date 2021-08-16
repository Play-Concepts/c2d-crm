from typing import Optional

from app.db.repositories.base import BaseRepository
from app.models.user import UserView

CREATE_PASSWORD_SQL = """
    UPDATE users SET hashed_password=crypt(:password, gen_salt('bf', 10)), is_verified=true
    WHERE email in (SELECT email FROM merchants WHERE password_change_token=:password_change_token)
    AND is_verified is false
    RETURNING id, email;
"""


class UsersRepository(BaseRepository):
    async def create_password(self, *, token: str, password: str) -> Optional[UserView]:
        query_values = {
            "password_change_token": token,
            "password": password,
        }
        updated_user = await self.db.fetch_one(
            query=CREATE_PASSWORD_SQL, values=query_values
        )
        return None if updated_user is None else UserView(**updated_user)
