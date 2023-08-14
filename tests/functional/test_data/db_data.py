from collections import namedtuple
from uuid import uuid4

PasswordAndHash = namedtuple('PasswordAndHash', 'password hash')

test_password_and_hash_pair = PasswordAndHash('hackme',
                                              r'f59a33e80babb1d53516302590fa7ff123f9ed533a54c'
                                              r'cab565924e84c8d271f46b4902a1a8fe21392e43e6de6c1'
                                              r'c21de91399ca73bdd3bed0b66dc14ec96c00')

test_user_info = {
    'id': str(uuid4()),
    'email': 'test_user@test_service.com',
    'password_hash': test_password_and_hash_pair.hash,
    'user_role_id': str(uuid4())
}
