from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends
from schemas import UserTimecodeSchema
from db.kafka import get_producer, CustomKafkaProducer
from core.auth import AuthorizedUserId

router = APIRouter()

VIEWS_TOPIC_NAME = 'views'


@router.post('/', description='Записать временную отметку на которой юзер остановился при просмотре')
async def add_movie_timecode(user_id: AuthorizedUserId,
                             validated: UserTimecodeSchema,
                             kafka_producer: CustomKafkaProducer = Depends(get_producer)):
    key = f'{user_id}+{validated.movie_id}'.encode()
    try:
        await kafka_producer.send(
            topic=VIEWS_TOPIC_NAME,
            key=key,
            value=str(validated.timestamp).encode()
        )
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=e.args[0].str())

    return HTTPStatus.OK
