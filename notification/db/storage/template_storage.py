from sqlalchemy import select
from db.postgres_connection import DbSessionDep
from db.models import Template
from db.storage.exceptions import TemplateNotFoundException


class TemplateStorage:
    def __init__(self, session: DbSessionDep) -> None:
        self._session = session

    async def get_by_name(self, name: str) -> Template:
        stmt = select(Template).where(Template.name == name)
        if template := (await self._session.execute(stmt)).first():
            return template[0]
        raise TemplateNotFoundException(name)
