import aiohttp

from uuid import UUID
from typing import Annotated

from aiohttp import ClientSession
from fastapi import Depends

from db.storage import UserStorageDep, ItemNotFoundException, DbConflictException
from db.model import UserProfile
from schemas.profile import UserProfileSchema, AvatarStatusesSchema, UserRatingStatsSchema, UserReviewsStatsSchema, \
    UserProfileResponseSchema, UserProfileUpdateSchema
from core.config import app_config
from core.logger import logger


class UserProfileServiceError(Exception):
    def __init__(self, message: str = 'Internal User Profile Service Error'):
        self.message = message


class UserProfileAlreadyExistsError(UserProfileServiceError):
    pass


class UserProfileNotFoundError(UserProfileServiceError):
    pass


class UserProfileService:
    def __init__(self, user_storage: UserStorageDep) -> None:
        self.storage = user_storage

    async def create_profile(self, data: UserProfileSchema, user_id: UUID):
        try:
            user = UserProfile(id=user_id, name=data.name, surname=data.surname, country=data.country,
                               time_zone=data.time_zone, phone_number=data.phone_number,
                               avatar_status=AvatarStatusesSchema.WITHOUT)
            await self.storage.generic.add(user)
        except DbConflictException:
            raise UserProfileAlreadyExistsError(message='Profile fir this user already exists')
        except Exception as exc:
            logger.error(str(exc))
            raise UserProfileServiceError(message='Can\'t process user profile.')

    async def update_profile(self, data: UserProfileUpdateSchema, user_id: UUID) -> None:
        try:
            user = await self.storage.generic.get(user_id)
            user.__dict__.update(data.model_dump())
            await self.storage.generic.update(user)
        except ItemNotFoundException:
            raise UserProfileNotFoundError(message='User profile not found.')

    async def get_profile(self, user_id: UUID, token: str):
        try:
            profile_data = await self.storage.generic.get(user_id)

            async with aiohttp.ClientSession() as session:
                rating_data = await self._make_request_to_social_api(session, token, app_config.rating_stats_url)
                rating_stats = UserRatingStatsSchema(
                    ratings=rating_data['ratings'],
                    total_count=rating_data['total_count'],
                    average_rating=rating_data['average_rating'],
                )

                reviews_data = await self._make_request_to_social_api(session, token, app_config.review_stats_url)
                reviews_stats = UserReviewsStatsSchema(
                    reviews=reviews_data['reviews'],
                    total_count=reviews_data['total_count'],
                    total_count_positive_reviews=reviews_data['total_count_positive_reviews'],
                    total_count_negative_reviews=reviews_data['total_count_negative_reviews'],
                    total_reviews_likes_count=reviews_data['total_reviews_likes_count'],
                    total_reviews_dislikes_count=reviews_data['total_reviews_dislikes_count'],
                )

            return UserProfileResponseSchema(
                name=profile_data.name,
                surname=profile_data.surname,
                country=profile_data.country,
                time_zone=profile_data.time_zone,
                phone_number=profile_data.phone_number,
                avatar_link=profile_data.avatar_link,
                avatar_status=profile_data.avatar_status,
                rating_stats=rating_stats,
                review_stats=reviews_stats,
            )

        except ItemNotFoundException:
            raise UserProfileNotFoundError(message='User profile not found.')

    async def destroy_profile(self, user_id: UUID) -> None:
        try:
            return await self.storage.generic.delete(user_id)
        except ItemNotFoundException:
            UserProfileNotFoundError(message='User profile not found.')

    @staticmethod
    async def _make_request_to_social_api(session: ClientSession, token: str, url: str):
        headers = {'Authorization': f'Bearer {token}'}
        async with session.get(url, headers=headers) as response:
            data = await response.json()

            return data


UserProfileServiceDep = Annotated[UserProfileService, Depends()]
