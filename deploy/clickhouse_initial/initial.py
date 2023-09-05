from clickhouse_driver import Client


client = Client(host='clickhouse-node1')
client.execute('CREATE DATABASE IF NOT EXISTS example ON CLUSTER company_cluster')
client.execute(
    '''CREATE TABLE example.regular_table ON CLUSTER company_cluster 
        (
            id Int64, 
            film UUID,
            user UUID,
            viewed_seconds Int32,
            created DateTime('Europe/Moscow'),
        ) Engine=MergeTree() ORDER BY id'''
)
