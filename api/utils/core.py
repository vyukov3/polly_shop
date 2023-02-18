import string
from secrets import choice as secrets_choice

from passlib.hash import pbkdf2_sha256


def generate_password():
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets_choice(alphabet) for _ in range(20))


def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pbkdf2_sha256.verify(password, hashed_password)
