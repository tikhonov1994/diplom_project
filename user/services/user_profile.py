from uuid import UUID
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException

from db.storage import UserStorageDep, ItemNotFoundException, DbConflictException
from db.model import UserProfile
from schemas.profile import UserProfileSchema, AvatarStatusesSchema


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
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Profile fir this user already exists')
        except Exception as exc:
            print(str(exc))
            raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail='Can\'t process user profile.')

    async def update_profile(self, data: UserProfileSchema, user_id: UUID) -> None:
        try:
            user = await self.storage.generic.get(user_id)
            user.__dict__.update(data.dict())
            await self.storage.generic.update(user)
        except ItemNotFoundException:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User profile not found.')

    async def get_profile(self, user_id: UUID) -> None:
        try:
            return await self.storage.generic.get(user_id)
        except ItemNotFoundException:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User profile not found.')

    async def destroy_profile(self, user_id: UUID) -> None:
        try:
            return await self.storage.generic.delete(user_id)
        except ItemNotFoundException:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User profile not found.')


UserProfileServiceDep = Annotated[UserProfileService, Depends()]
