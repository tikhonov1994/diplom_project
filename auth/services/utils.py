import os
import hashlib

from db.model import UserInfo


def generate_hashed_password(password: str):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

    return key + salt


def check_password(pass_to_check: str, user: UserInfo):
    password = user.password_hash
    salt = password[-32:]
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        pass_to_check.encode('utf-8'),  # Конвертирование пароля в байты
        salt,
        100000
    )
    if (new_key + salt) == password:
        return True
    else:
        return False
