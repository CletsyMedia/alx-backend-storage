#!/usr/bin/env python3
"""
Defines a Cache class that interacts with Redis.
"""
import redis
import uuid
from typing import Union

class Cache:
    """
    Cache class interacts with Redis to store and retrieve data.
    """

    def __init__(self) -> None:
        """
        Initializes the Cache instance with a Redis client.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis and returns the generated key.
        
        Args:
            data: Data to be stored. Can be str, bytes, int, or float.
        
        Returns:
            str: Generated key used to store the data in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

