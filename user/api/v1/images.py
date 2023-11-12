from contextlib import closing
from http import HTTPStatus

from fastapi import APIRouter, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from core.auth import AuthorizedUserId
from schemas.image import UserImageSchema
from services import ImagesServiceDep
from services.images import ImageServiceError, UserNotFoundError, AvatarAlreadyUserError

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

    try:
        with closing(image.file) as file:
            img_schema = UserImageSchema(user_id=user_id,
                                         data=file.read(),
                                         mime=image.content_type,
                                         name=image.filename)
        await service.handle_new_user_image(img_schema, tasks)
        return JSONResponse(status_code=HTTPStatus.ACCEPTED,
                            content='New avatar processing started.')
    except AvatarAlreadyUserError as err:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=err.message)
    except UserNotFoundError as err:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=err.message)
    except ImageServiceError as err:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail=err.message)
