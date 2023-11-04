from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException, BackgroundTasks

from adapters import FileStorageDep, NsfwCheckerDep
from db.storage import UserStorageDep, ItemNotFoundException, DbConflictException
from db.model import UserProfile
from schemas.image import UserImageSchema


class ImagesService:
    def __init__(self,
                 file_storage: FileStorageDep,
                 user_storage: UserStorageDep,
                 checker: NsfwCheckerDep) -> None:
        self.file_storage = file_storage
        self.user_storage = user_storage
        self.checker = checker

    async def handle_new_user_image(self,
                                    image: UserImageSchema,
                                    tasks: BackgroundTasks) -> None:
        try:
            user = await self.user_storage.generic.get(image.user_id)
            user.avatar_status = 'ON_INSPECTION'
            await self.user_storage.generic.update(user)
            tasks.add_task(self._process_new_image_in_background, user, image)
        except ItemNotFoundException:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found.')

    async def _process_new_image_in_background(self, user: UserProfile, image: UserImageSchema) -> None:
        check_result = await self.checker.check(image)
        try:
            user.avatar_link = self.file_storage.save(image.name, image.data, image.mime)
            user.avatar_status = check_result.value
            await self.user_storage.generic.update(user)
        except DbConflictException:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Two users can\'t have the same avatar.')
        except Exception:
            raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail='Can\'t process new user image.')


ImagesServiceDep = Annotated[ImagesService, Depends()]
