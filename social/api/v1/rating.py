from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette import status

from core.auth import UserIdDep
from services import MovieRatingServiceDep
from services.rating import MovieRatingNotFound
from schemas.rating import AssessMovieSchema, RateMovieSchema, MovieRatingStats

router = APIRouter()


@router.post('/movie/rate',
             description='Оценить фильм.')
async def rate_movie(rate_data: RateMovieSchema,
                     service: MovieRatingServiceDep,
                     user_id: UserIdDep):
    await service.set_rating(rate_data.movie_id,
                             user_id,
                             rate_data.rating_value)


@router.post('/movie/like',
             description='Поставить лайк фильму.')
async def like_movie(like_data: AssessMovieSchema,
                     service: MovieRatingServiceDep,
                     user_id: UserIdDep):
    await service.like(like_data.movie_id, user_id)


@router.post('/movie/dislike',
             description='Поставить дизлайк фильму.')
async def dislike_movie(dislike_data: AssessMovieSchema,
                        service: MovieRatingServiceDep,
                        user_id: UserIdDep):
    await service.dislike(dislike_data.movie_id, user_id)


@router.delete('/movie/rate',
               description='Удалить оценку фильма.')
async def delete_movie_rating(deletion_data: AssessMovieSchema,
                              service: MovieRatingServiceDep,
                              user_id: UserIdDep):
    await service.remove_rating(deletion_data.movie_id, user_id)


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
