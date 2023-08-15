from typing import Annotated

from fastapi import Depends

from db.storage.abstract_storage import AbstractStorage
from db.storage.elastic_storage import ElasticStorage

StorageDep = Annotated[AbstractStorage, Depends(ElasticStorage)]
