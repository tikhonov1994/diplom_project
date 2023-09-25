from uuid import UUID

from core.auth import UserIdDep
from fastapi import APIRouter, HTTPException
from schemas.rating import MovieRatingStats, RateMovieSchema
from services.rating import MovieRatingNotFound
from starlette import status

from services import MovieRatingServiceDep

from core.logger import logger

router = APIRouter()


@router.post('/movie/rate',
             description='Оценить фильм.')
async def rate_movie(rate_data: RateMovieSchema,
                     service: MovieRatingServiceDep,
                     user_id: UserIdDep):
    await service.set_rating(rate_data.movie_id,
                             str(user_id),
                             rate_data.rating_value)


@router.post('/movie/{movie_id}/like',
             description='Поставить лайк фильму.')
async def like_movie(movie_id: UUID,
                     service: MovieRatingServiceDep,
                     user_id: UserIdDep):
    await service.like(movie_id, user_id)


@router.post('/movie/{movie_id}/dislike',
             description='Поставить дизлайк фильму.')
async def dislike_movie(movie_id: UUID,
                        service: MovieRatingServiceDep,
                        user_id: UserIdDep):
    await service.dislike(movie_id, user_id)


@router.delete('/movie/{movie_id}/rate',
               description='Удалить оценку фильма.')
async def delete_movie_rating(movie_id: UUID,
                              service: MovieRatingServiceDep,
                              user_id: UserIdDep):
    await service.remove_rating(movie_id, user_id)


@router.get('/movie/{movie_id}',
            description='Получить данные рейтинга для фильма.',
            response_model=MovieRatingStats)
async def get_movie_rating_stats(movie_id: UUID,
                                 service: MovieRatingServiceDep,
                                 _: UserIdDep) -> MovieRatingStats:
    try:
        return await service.get_rating(movie_id)
    except MovieRatingNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
