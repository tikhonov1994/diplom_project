import logging
from typing import Any
from uuid import UUID

from elasticsearch import NotFoundError
from fastapi import HTTPException
from starlette import status

from db.storage.abstract_storage import AbstractStorage, CollectionResultType, NestedObjectFilter
from db.storage.backends import ElasticDep


class ElasticStorage(AbstractStorage):
    def __init__(self, elastic: ElasticDep) -> None:
        self._elastic = elastic

    async def get(self, collection: str, item_id: UUID) -> CollectionResultType | None:
        try:
            doc = await self._elastic.get(index=collection, id=str(item_id))
        except NotFoundError:
            return None
        return doc['_source']

    async def search(
            self,
            collection: str,
            page_number: int,
            page_size: int,
            search_queries: list[tuple[str, str]] | None = None,
            sort_by: str | None = None,
            nested_object_filter: NestedObjectFilter | None = None) -> tuple[int, list[CollectionResultType]]:
        if page_number * page_size > 10000:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Value=(page_number*page_size) must be less than 10\'000')

        es_query = self._build_pagination_query(page_number, page_size)
        if search_queries:
            es_query |= self._build_search_query(search_queries)
        if sort_by:
            es_query |= self._build_sort_query(sort_by)
        if nested_object_filter:
            es_query |= self._build_nested_filter_query(nested_object_filter)

        search_results = await self._elastic.search(index=collection, **es_query)
        total_items = int(search_results['hits']['total']['value'])
        return total_items, [result['_source'] for result in search_results['hits']['hits']]

    async def get_many(self, collection: str, id_list: list[UUID]) -> list[CollectionResultType]:
        _query = {'ids': id_list}
        search_results = await self._elastic.mget(index=collection, body=_query)
        results = []
        for result in search_results['docs']:
            if not result['found']:
                logging.warning('Found non-consistent item with id=\'%s\'', result["_id"])
                continue
            results.append(result['_source'])
        return results

    @staticmethod
    def _build_pagination_query(page_number: int,
                                page_size: int) -> dict[str, Any]:
        return {
            'size': page_size,
            'from_': (page_number - 1) * page_size,
        }

    @staticmethod
    def _build_search_query(search_queries: list[tuple[str, str]]) -> dict[str, Any]:
        match_list = [
            {
                'match': {
                    search_field: {
                        'query': search_val,
                        'fuzziness': 'AUTO'
                    }
                }
            }
            for search_field, search_val in search_queries
        ]

        return {
            'query': {
                'bool': {
                    'should': match_list,
                    'minimum_should_match': 1
                }
            }
        }

    @staticmethod
    def _build_sort_query(sort_by: str) -> dict[str, Any]:
        return {
            'sort': [{sort_by[1:]: 'desc'}] if sort_by[0] == '-' else [{sort_by: 'asc'}]
        }

    @staticmethod
    def _build_nested_filter_query(
            nested_object_filter: NestedObjectFilter) -> dict[str, Any]:
        return {
            'query': {
                'nested': {
                    'path': nested_object_filter.name,
                    'query': {
                        'bool': {
                            'filter': [
                                {
                                    'term': {
                                        f'{nested_object_filter.name}.{nested_object_filter.field}':
                                            nested_object_filter.value
                                    }
                                }
                            ]
                        }
                    },
                    'score_mode': 'avg'
                }
            }
        }
