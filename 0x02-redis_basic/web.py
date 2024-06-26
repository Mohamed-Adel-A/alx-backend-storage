#!/usr/bin/env python3
"""
Web cache module
"""
import requests
import redis
from datetime import timedelta


def get_page(url: str) -> str:
    """
    Retrieve HTML content of a URL and cache the result
    """

    if url is None:
        return ""

    # Connect to Redis
    r = redis.Redis()

    # Count increments when get_page is called
    r.incr(f'count:{url}')

    # Check if the URL is already cached
    cached_html = r.get(f'result:{url}')
    if cached_html:
        return str(cached_html)

    # Fetch the HTML content from the URL
    response = requests.get(url)
    html_content = response.content.decode('utf-8')

    # Cache the HTML content with expiration time of 10 seconds
    r.setex(f'result:{url}',
            timedelta(seconds=10), html_content)

    # Track the number of times the URL is accessed
    count_key = f"count:{url}"
    r.set(count_key, 0)

    return str(html_content)
