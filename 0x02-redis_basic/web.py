#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker.
"""

import requests
import redis
from typing import Optional

# Initialize Redis client
redis_client = redis.Redis()


def get_page(url: str) -> str:
    """
    Retrieve the HTML content of a URL and cache it with an expiration time of 10 seconds.
    Track the number of times the URL was accessed.

    Args:
        url (str): The URL to fetch the HTML content from.

    Returns:
        str: The HTML content of the URL.
    """
    # Track the number of times the URL was accessed
    redis_client.incr(f"count:{url}")

    # Check if the URL content is cached
    cached_content = redis_client.get(url)
    if cached_content:
        return cached_content.decode("utf-8")

    # Fetch the HTML content from the URL
    response = requests.get(url)
    html_content = response.text

    # Cache the HTML content with an expiration time of 10 seconds
    redis_client.setex(url, 10, html_content)

    return html_content


if __name__ == "__main__":
    # Test the get_page function
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/https://www.example.com"
    html_content = get_page(url)
    print(html_content)

