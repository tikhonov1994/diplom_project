from typing import Annotated

from fastapi import Depends
from elasticsearch import AsyncElasticsearch

es: AsyncElasticsearch | None = None


async def get_elastic() -> AsyncElasticsearch:
    return es


ElasticDep = Annotated[AsyncElasticsearch, Depends(get_elastic)]
