#!/usr/bin/env python3
"""
A module for implementing an expiring web cache and tracker.
"""

import requests
import redis
from typing import Callable

# Initialize Redis client
redis_store = redis.Redis()


def cache_and_track(method: Callable) -> Callable:
    """
    Decorator to cache the output of fetched data and track URL accesses.
    """
    def wrapper(url: str) -> str:
        """
        Wrapper function for caching and tracking URL accesses.
        """
        # Track URL access count
        redis_store.incr(f'count:{url}')

        # Check if URL content is cached
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')

        # Fetch URL content
        response = method(url)
        content = response.text

        # Cache URL content with expiration time of 10 seconds
        redis_store.setex(f'result:{url}', 10, content)

        return content

    return wrapper


@cache_and_track
def get_page(url: str) -> str:
    """
    Retrieves the HTML content of a URL and returns it.
    """
    return requests.get(url)


if __name__ == "__main__":
    # Example usage
    print(get_page("http://slowwly.robertomurray.co.uk/delay/1000/url/https://example.com"))
