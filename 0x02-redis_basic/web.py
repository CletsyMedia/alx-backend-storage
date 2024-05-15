#!/usr/bin/env python3
"""
A module with tools for request caching and tracking.
"""
import redis
import requests
from functools import wraps
from typing import Callable

# Initialize Redis client
redis_store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    """
    Decorator to cache the output of fetched data and track the
    number of times a URL was accessed.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper function for caching the output and tracking the request.
        """
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@data_cacher
def get_page(url: str) -> str:
    """
    Fetches the content of a URL using requests module and
    caches the response.
    """
    return requests.get(url).text


if __name__ == "__main__":
    # Example usage
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/https://www.example.com"
    html_content = get_page(url)
    print(html_content)
