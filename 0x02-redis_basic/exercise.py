#!/usr/bin/env python3
"""
Redis basic
"""

import uuid
import redis
from typing import Union

class Cache:
    """
    Cache class
    """
    def __init__(self):
        """
        Initialize Cache class
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn=None) -> Union[str, bytes, int, float]:
        """
        Retrieve data from Redis
        """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

def count_calls(method):
    """
    Decorator to count method calls
    """
    import functools

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper

def call_history(method):
    """
    Decorator to store history of inputs and outputs
    """
    import functools

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function
        """
        inputs_key = "{}:inputs".format(method.__qualname__)
        outputs_key = "{}:outputs".format(method.__qualname__)

        self._redis.rpush(inputs_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, str(result))

        return result

    return wrapper

