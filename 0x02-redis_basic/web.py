#!/usr/bin/env python3
"""
Web cache module
"""
import requests
import redis
from typing import Callable
from functools import wraps


# Connect to Redis
r = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    '''
    Caches the output of fetched data.
    '''
    @wraps(method)
    def invoker(url) -> str:
        '''
        The wrapper function for caching the output.
        '''
        r.incr(f'count:{url}')
        result = r.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        content = method(url)
        r.set(f'count:{url}', 0)
        r.setex(f'result:{url}', 10, content)
        return content
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''
    Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    response = requests.get(url)
    html_content = response.text
    return html_content
