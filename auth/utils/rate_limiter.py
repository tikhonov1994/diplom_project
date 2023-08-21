import datetime
from db.redis import get_redis
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from starlette import status

# Установим лимит на 20 запросов в минуту
REQUEST_LIMIT_PER_MINUTE = 20


def throttle(app: FastAPI) -> None:
    @app.middleware('http')
    async def before_request(request: Request, call_next):
        redis_conn = await get_redis()
        pipe = redis_conn.pipeline()
        now = datetime.datetime.now()
        identifier = request.headers.get('Authorization')
        key = f'{identifier}:{now.minute}'
        await pipe.incr(key, 1)
        await pipe.expire(key, 59)
        result = await pipe.execute()
        request_number = result[0]
        if request_number > REQUEST_LIMIT_PER_MINUTE:
            return ORJSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={'detail': 'Too many requests'}
            )

        response = await call_next(request)
        return response