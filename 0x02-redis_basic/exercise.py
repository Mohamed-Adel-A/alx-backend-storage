#!/usr/bin/env python3
"""
Module to interact with Redis as a cache
"""
import redis
import uuid
from typing import Union

class Cache:
    """
    Cache class to interact with Redis
    """

    def __init__(self) -> None:
        """
        Initializes the Redis client and flushes the database
        """
        self._redis: redis.Redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis with a randomly generated key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

# Testing
if __name__ == "__main__":
    cache = Cache()
    data = b"hello"
    key = cache.store(data)
    print(key)

    local_redis = redis.Redis()
    print(local_redis.get(key))
