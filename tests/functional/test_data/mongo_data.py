from datetime import datetime
from random import randint, choice
from uuid import uuid4

from functional.test_data.db_data import test_user_info, test_admin_info

test_movie_ids = [uuid4() for _ in range(5)]
user_ids = [test_admin_info.get('id'),
            test_user_info.get('id')]

test_movieLikes = [
    {
        'user_id': choice(user_ids),
        'entity_id': choice(test_movie_ids),
        'value': randint(0, 10),
        'added': datetime.now()
    }
    for _ in range(20)
]
