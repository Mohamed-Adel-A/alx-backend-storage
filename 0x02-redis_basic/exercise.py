#!/usr/bin/env python3
"""
Cache module to interact with Redis
"""
import redis
import uuid
import functools
from typing import Union, Callable

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

    def get(self, key: str, fn: Callable = None):
        """
        Retrieves data from Redis and optionally converts it back to the original type
        """
        data = self._redis.get(key)
        if data is None:
            return None
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

    def replay(self, method):
        """
        Displays the history of calls of a particular function
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        inputs = self._redis.lrange(input_key, 0, -1)
        outputs = self._redis.lrange(output_key, 0, -1)
        print(f"{method.__qualname__} was called {len(inputs)} times:")
        for input_, output in zip(inputs, outputs):
            print(f"{method.__qualname__}(*{input_.decode()}) -> {output.decode()}")

    def __call_history(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            input_key = f"{method.__qualname__}:inputs"
            output_key = f"{method.__qualname__}:outputs"
            self._redis.rpush(input_key, str(args))
            result = method(self, *args, **kwargs)
            self._redis.rpush(output_key, str(result))
            return result
        return wrapper

    def __count_calls(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper

    @__count_calls
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
    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value

    cache.store("first")
    print(cache.store.__qualname__, cache._redis.get(cache.store.__qualname__))

    cache.store("second")
    cache.store("third")
    print(cache.store.__qualname__, cache._redis.get(cache.store.__qualname__))

    s1 = cache.store("first")
    print(s1)
    s2 = cache.store("second")
    print(s2)
    s3 = cache.store("third")
    print(s3)

    inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
    outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

    print("inputs: {}".format(inputs))
    print("outputs: {}".format(outputs))
