from sqlalchemy import select
from uuid import UUID

from db.storage.generic_storage import GenericStorageMixin
from db.storage.session import DbSessionDep
from db.model import UserSocial, UserInfo
from utils.tracer import sub_span


class UserSocialStorage(GenericStorageMixin):
    def __init__(self, session: DbSessionDep):
        super().__init__(UserSocial, session)
        self._session = session

    @sub_span
    async def add_user_social(self, user_social: UserSocial) -> None:
        await self.generic.add(user_social)
    
    @sub_span
    async def get_user_by_social_id(self, social_id: str) -> UserInfo:
        stmt = select(UserSocial).where(UserSocial.social_id == social_id,
                                        UserSocial.social_name=='yandex')
        if social := (await self._session.execute(stmt)).first():
            return social[0]['user_info_id']
        return None
    
    @sub_span
    async def create_user_social(self, user_id: UUID, social_id: str):
        user_social = UserSocial(user_info_id=user_id, social_name='yandex', social_id=social_id)
        await self.generic.add(user_social)
