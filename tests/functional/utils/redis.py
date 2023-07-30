from redis import Redis


def clear_cache(redis_client: Redis) -> None:
    redis_client.flushall()
