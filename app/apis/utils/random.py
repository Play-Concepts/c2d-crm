import secrets
import string
from hashlib import md5
from typing import Optional


def random_string(length: int = 20) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for i in range(length))


def random_hash(hash_str: Optional[str] = None) -> str:
    target = random_string() if hash_str is None else hash_str
    return md5(target.encode()).hexdigest()
