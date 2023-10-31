from contextlib import closing
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from services import ImagesServiceDep
from adapters import NsfwCheckResult
from schemas.image import UserImageSchema

router = APIRouter()


@router.post('/{user_id}/avatar',
             description='Обновить аватар пользователя')
async def add_user_avatar(user_id: UUID,
                          image: UploadFile,
                          service: ImagesServiceDep) -> JSONResponse:
    if image.content_type.find('image') == -1:
        raise HTTPException(status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                            detail='Bad Avatar mime-type (should be \'image\').')
    with closing(image.file) as file:
        img_schema = UserImageSchema(user_id=user_id,
                                     data=file.read(),
                                     mime=image.content_type,
                                     name=image.filename)
    if await service.handle_new_user_image(img_schema) != NsfwCheckResult.accepted:
        return JSONResponse(status_code=HTTPStatus.NOT_ACCEPTABLE,
                            content={'detail': 'User Avatar content is not acceptable.'})
    return JSONResponse(status_code=HTTPStatus.OK,
                        content={'detail': 'User Avatar changed successfully.'})
