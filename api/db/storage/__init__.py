from typing import Annotated

from fastapi import Depends

from db.storage.abstract_storage import AbstractStorage, NestedObjectFilter
from db.storage.elastic_storage import ElasticStorage

StorageDep = Annotated[AbstractStorage, Depends(ElasticStorage)]

__all__ = ['StorageDep', NestedObjectFilter, AbstractStorage, ElasticStorage]
