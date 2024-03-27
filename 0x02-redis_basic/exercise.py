#!/usr/bin/env python3
"""This module contains the
implementation of
the Cache class
"""
import redis
import uuid
from typing import Union


class Cache:
    def __init__(self):
        "Initializes the cache with an empty database"
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """To store the data in the cache"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
