#!/usr/bin/env python3
"""
Web Cache
"""

import requests
import redis
import time

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
        return cached_page

    # Retrieve page from the web
    response = requests.get(url)
    if response.status_code == 200:
        page_content = response.text
        redis_client.setex(page_key, 10, page_content)  # Cache with expiration time
        redis_client.incr(count_key)
        return page_content
    else:
        return f"Error: Failed to retrieve page - Status code {response.status_code}"

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/https://www.google.com"
    print(get_page(url))
    time.sleep(2)
    print(get_page(url))
