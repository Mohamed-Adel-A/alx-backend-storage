#!/usr/bin/env python3
"""
Web Cache
"""

import requests
import redis
import time
from typing import Callable

def get_page(url: str) -> str:
    """
    Retrieve HTML content of a URL
    """
    redis_client = redis.Redis()
    page_key = f"page:{url}"
    count_key = f"count:{url}"

    # Check if page is cached
    cached_page = redis_client.get(page_key)
    if cached_page:
        redis_client.incr(count_key)
        return cached_page.decode('utf-8')  # Decoding bytes to str

    # Retrieve page from the web
    response = requests.get(url)
    if response.status_code == 200:
        page_content = response.text
        redis_client.setex(page_key, 10, page_content)  # Cache with expiration time
        redis_client.incr(count_key)
        time.sleep(10)  # Wait for 10 seconds
        redis_client.delete(page_key)  # Remove page from cache after 10 seconds
        return page_content
    else:
        return f"Error: Failed to retrieve page - Status code {response.status_code}"

if __name__ == "__main__":
    url = "http://google.com"
    print(get_page(url))  # First call to cache
    print(get_page(url))  # Second call should be retrieved from cache
    print(get_page(url))  # Third call should trigger removal from cache
    print(get_page(url))  # Fourth call should not find the page in cache
