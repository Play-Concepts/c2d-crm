from typing import Dict, List

from .submod import rand_gen
import uuid

class User:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name


def fn_list_users() -> List[User]:
    return [User(uuid.uuid4().__str__(), 'terry'), User(uuid.uuid4().__str__(), 'thanny'), User(uuid.uuid4().__str__(), 'jenny')]


def fn_get_user(user_id: str) -> User:
    return User(user_id, 'terry')
