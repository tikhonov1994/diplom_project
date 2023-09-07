from clickhouse_driver import Client


client = Client(host='clickhouse1')
client.execute('CREATE DATABASE IF NOT EXISTS example;')
client.execute(
    '''CREATE TABLE example.regular_table
        (
            id Int64, 
            film UUID,
            user UUID,
            viewed_seconds Int32,
            created DateTime('Europe/Moscow')
        ) Engine=MergeTree() ORDER BY id;'''
)
