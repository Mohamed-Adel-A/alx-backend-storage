#!/usr/bin/env python3
"""
Redis basic
"""

import uuid
import redis
from typing import Union, Any, Callable


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count method calls
    """
    import functools

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Wrapper function
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store history of inputs and outputs
    """
    import functools

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
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


def replay(method: Callable) -> None:
    '''
    Displays the history of calls of a particular function
    '''
    if method is None or not hasattr(method, '__self__'):
        return
    redis_store = getattr(method.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = method.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


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

    @call_history
    @count_calls
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

    def get_str(self, key: str):
        """
        Retrieves data from Redis and decodes it as UTF-8
        """
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str):
        """
        Retrieves data from Redis and converts it to an integer
        """
        return self.get(key, fn=int)
