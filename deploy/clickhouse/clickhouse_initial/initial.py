from clickhouse_driver import Client

client = Client(host='clickhouse1')
client.execute('CREATE DATABASE IF NOT EXISTS ugc;')
client.execute(
    '''CREATE TABLE IF NOT EXISTS ugc.views
        (
            id UUID, 
            movie_id UUID,
            user_id UUID,
            ts Int32,
            created Int64
        ) Engine=MergeTree() ORDER BY created;'''
)
