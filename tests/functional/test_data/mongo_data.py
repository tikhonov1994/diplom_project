import string
from datetime import datetime, timedelta
from random import choice, randint, random
from uuid import uuid4

from functional.test_data.db_data import test_admin_info, test_user_info

test_movie_ids = [uuid4() for _ in range(3)]
test_review_ids = [uuid4() for _ in range(30)]
letters = string.ascii_lowercase
user_ids = [test_admin_info.get('id'),
            test_user_info.get('id')]

test_movieLikes = [
    {
        'user_id': choice(user_ids),
        'entity_id': choice(test_movie_ids),
        'value': randint(0, 10),
        'added': datetime.now()
    }
    for _ in range(30)
]


def gen_datetime(min_year=1900, max_year=datetime.now().year):
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random()


test_reviews_data = [
    {
        'review_id': choice(test_review_ids),
        'film_id': choice(test_movie_ids),
        'text': ''.join(choice(letters) for _ in range(randint(10, 100))),
        'added': gen_datetime(),
        'user_id': choice(user_ids),
        'author_rating': randint(0, 10),
    }
    for _ in range(30)
]


test_reviews_assessments_data = [
    {
        'review_id': test_reviews_data[i].get('review_id'),
        'user_id': user_ids[0],
        'liked': True,
    }
    for i in range(30)
]
