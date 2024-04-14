#!/usr/bin/env python3
"""
Web cache module
"""
import requests
import redis

def get_page(url: str) -> str:
    """
    Retrieve HTML content of a URL and cache the result
    """
    # Connect to Redis
    r = redis.Redis()

    # Check if the URL is already cached
    cached_html = r.get(url)
    if cached_html:
        return cached_html.decode('utf-8')

    # Fetch the HTML content from the URL
    response = requests.get(url)
    html_content = response.text

    # Cache the HTML content with expiration time of 10 seconds
    r.setex(url, 10, html_content)

    # Track the number of times the URL is accessed
    count_key = f"count:{url}"
    r.incr(count_key)

    return html_content

if __name__ == "__main__":
    # Test the get_page function
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com"
    for _ in range(5):
        print(get_page(url))
