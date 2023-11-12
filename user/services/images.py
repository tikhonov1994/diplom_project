from typing import Annotated

from fastapi import Depends, BackgroundTasks

from adapters import FileStorageDep, NsfwCheckerDep, NsfwCheckResult
from db.storage import UserStorageDep, ItemNotFoundException, DbConflictException
from db.model import UserProfile
from schemas.image import UserImageSchema


class ImageServiceError(Exception):
    def __init__(self, message: str = 'Internal Image Service Error') -> None:
        self.message = message


class UserNotFoundError(ImageServiceError):
    pass


class AvatarAlreadyUserError(ImageServiceError):
    pass


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
            raise UserNotFoundError(message='User not found.')

    async def _process_new_image_in_background(self, user: UserProfile, image: UserImageSchema) -> None:
        check_result = await self.checker.check(image)
        try:
            _old_link = user.avatar_link
            user.avatar_link = self.file_storage.save(image.name, image.data, image.mime) \
                if check_result == NsfwCheckResult.accepted \
                else None
            user.avatar_status = check_result.value
            await self.user_storage.generic.update(user)
            if _old_link:
                *_, avatar_file_name = str(_old_link).split('/')
                self.file_storage.delete(avatar_file_name)
        except DbConflictException:
            raise AvatarAlreadyUserError(message='Two users can\'t have the same avatar.')
        except Exception:
            raise ImageServiceError(message='Can\'t process new user image.')


ImagesServiceDep = Annotated[ImagesService, Depends()]
