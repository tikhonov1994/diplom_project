from uuid import UUID
from db.storage import ReviewStorageDep
from models.review import ReviewRating
from schemas.reviews_query import QueryParams


class ReviewService:
    TOP_DAILY_REVIEWS_COUNT = 5

    def __init__(self, mongo_storage: ReviewStorageDep) -> None:
        self.mongo_storage = mongo_storage

    async def add_review(self, text: str, user_id: UUID, film_id: UUID, author_rating: int):
        await self.mongo_storage.insert_review(text, user_id, author_rating, film_id)

    async def update_review(self, text: str, user_id: UUID, author_rating: int, film_id: UUID,
                            review_id: UUID) -> None:
        await self.mongo_storage.update_review(text, user_id, author_rating, film_id, review_id)

    async def get_reviews(self, query_params: QueryParams):
        sort_params = query_params.order.value.split('_')
        if sort_params[-1] == 'asc':
            sort = ('_'.join(sort_params[:-1]), 1)
        elif sort_params[-1] == 'desc':
            sort = ('_'.join(sort_params[:-1]), -1)
        else:
            sort = None
        if filter_field := query_params.filter_field:
            if (filter_field.value == 'added' and query_params.filter_argument and query_params.date_value):
                filter_query = {filter_field.value: {('$' + query_params.filter_argument.value): query_params.date_value}}
            elif (filter_field.value == 'author_rating' and query_params.filter_argument and query_params.rating_value):
                filter_query = {filter_field.value: {('$' + query_params.filter_argument.value): query_params.rating_value}}
            else:
                raise
        else:
            filter_query = None
        return await self.mongo_storage.get_reviews(sort, filter_query)

    async def delete_review(self, review_id: UUID):
        await self.mongo_storage.delete_review(review_id)

    async def add_assessment_to_review(self, review_id: UUID, user_id: UUID, liked: bool):
        await self.mongo_storage.upset_assessment(liked, user_id, review_id)

    async def delete_assessment_review(self, review_id: UUID, user_id: UUID):
        await self.mongo_storage.delete_assessment(user_id, review_id)

    async def get_review_rating(self, review_id: UUID) -> ReviewRating:
        return await self.mongo_storage.get_review_rating(review_id)

    async def get_daily_top_reviews(self):
        return await self.mongo_storage.get_most_liked_daily_reviews(self.TOP_DAILY_REVIEWS_COUNT)
