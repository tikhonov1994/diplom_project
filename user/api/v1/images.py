from contextlib import closing
from http import HTTPStatus

from fastapi import APIRouter, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from core.auth import AuthorizedUserId
from schemas.image import UserImageSchema
from services import ImagesServiceDep

router = APIRouter()


@router.post('/user-avatar',
             description='Обновить аватар пользователя')
async def add_user_avatar(user_id: AuthorizedUserId,
                          image: UploadFile,
                          service: ImagesServiceDep,
                          tasks: BackgroundTasks) -> JSONResponse:
    if image.content_type.find('image') == -1:
        raise HTTPException(status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                            detail='Bad Avatar mime-type (should be \'image\').')
    with closing(image.file) as file:
        img_schema = UserImageSchema(user_id=user_id,
                                     data=file.read(),
                                     mime=image.content_type,
                                     name=image.filename)
    await service.handle_new_user_image(img_schema, tasks)
    return JSONResponse(status_code=HTTPStatus.ACCEPTED,
                        content='New avatar processing started.')
