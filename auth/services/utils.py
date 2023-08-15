import os
import hashlib

from db.model import UserInfo


def generate_hashed_password(password: str) -> str:
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return (key + salt).hex()


def check_password(pass_to_check: str, user: UserInfo) -> bool:
    password = user.password_hash
    salt = bytes.fromhex(password)[-32:]
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        pass_to_check.encode('utf-8'),
        salt,
        100000
    )
    if (new_key + salt).hex() == password:
        return True
    else:
        return False
