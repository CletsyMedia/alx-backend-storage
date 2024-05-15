#!/usr/bin/env python3
"""
A simple cache using Redis.
"""

from typing import Callable, Optional, Union
import redis
from uuid import uuid4
from functools import wraps

# Initialize Redis client
redis_store = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of times a method is called."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function for counting calls."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs of a method."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function for storing history."""
        input_str = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input_str)
        output_str = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output_str)
        return output_str

    return wrapper


class Cache:
    """A Cache class using Redis."""

    def __init__(self):
        """Initialize the Cache instance."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis and return the generated key."""
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(
    self, 
    key: str, 
    fn: Optional[Callable] = None
) -> Union[str, bytes, int, float]:

        """Retrieve data from Redis using the provided key."""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Retrieve data from Redis as a string."""
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """Retrieve data from Redis as an integer."""
        value = self._redis.get(key)
        return int(value.decode("utf-8")) if value else 0


def replay(fn: Callable) -> None:
    """Display the history of calls of a particular function."""
    r = redis.Redis()
    function_name = fn.__qualname__
    value = r.get(function_name)
    try:
        value = int(value.decode("utf-8"))
    except Exception:
        value = 0

    print("{} was called {} times:".format(function_name, value))
    inputs = r.lrange("{}:inputs".format(function_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(function_name), 0, -1)

    for input_data, output_data in zip(inputs, outputs):
        input_str = input_data.decode("utf-8") if input_data else ""
        output_str = output_data.decode("utf-8") if output_data else ""
        print("{}(*{}) -> {}".format(function_name, input_str, output_str))


if __name__ == "__main__":
    cache = Cache()
    cache.store("foo")
    cache.store("bar")
    cache.store(42)
    replay(cache.store)
