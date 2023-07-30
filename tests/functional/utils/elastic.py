import logging
from uuid import UUID

from elasticsearch import helpers, Elasticsearch, AsyncElasticsearch

from functional.test_data.es_data import index_list


def clear_indices(es_client: Elasticsearch) -> None:
    for idx in index_list:
        es_client.delete_by_query(index=idx, query={'match_all': {}})


def refresh_indices(es_client: Elasticsearch) -> None:
    for idx in index_list:
        es_client.indices.refresh(index=idx)
        es_client.indices.refresh(index=idx)
        es_client.indices.refresh(index=idx)


def insert_data_to_index(es_client: Elasticsearch, index_name: str, data_rows: list[dict[str, any]]) -> None:
    actions = [{'_index': index_name, '_id': row['id'], '_source': row} for row in data_rows]
    row_count, errors = helpers.bulk(es_client, actions)
    if errors:
        logging.error('Failed to insert data to index \'%s\'.', index_name)
    logging.info('Inserted %d rows to index \'%s\'', row_count, index_name)


async def add_document_to_index(
        es_client: AsyncElasticsearch,
        index: str,
        id_: UUID,
        document: dict[str, any]) -> None:
    await es_client.indices.refresh(index=index)
    await es_client.index(index=index,
                          id=str(id_),
                          document=document)


async def delete_document_from_index(
        es_client: AsyncElasticsearch,
        index: str,
        id_: UUID) -> None:
    await es_client.indices.refresh(index=index)
    await es_client.delete_by_query(index=index,
                                    query={'match': {'id': str(id_)}})
