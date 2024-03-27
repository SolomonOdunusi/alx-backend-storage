#!/usr/bin/env python3
"""This module contains the
implementation of
the Cache class
"""
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Counts uniquely the num of times a method is called"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper to conserve functionality"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """ The decorator to store the history of calls of a function
    that is both input and output
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper to conserve functionality"""
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)

        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output

    return wrapper


def replay(fn: Callable):
    """Display the history of calls of a function
    for both input and output"""
    r = redis.Redis()
    f_name = fn.__qualname__
    n_calls = r.get(f_name)
    try:
        n_calls = n_calls.decode('utf-8')
    except Exception:
        n_calls = 0
    print(f'{f_name} was called {n_calls} times:')

    ins = r.lrange(f_name + ":inputs", 0, -1)
    outs = r.lrange(f_name + ":outputs", 0, -1)

    for i, o in zip(ins, outs):
        try:
            i = i.decode('utf-8')
        except Exception:
            i = ""
        try:
            o = o.decode('utf-8')
        except Exception:
            o = ""

        print(f'{f_name}(*{i}) -> {o}')


class Cache:
    """ Class to cache data to redis"""
    def __init__(self):
        """Initializes the cache with an empty database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """To store the data in the cache"""
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)

        return random_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """To get the value from the cache using the key"""
        value = self._redis.get(key)
        if fn:
            value = fn(value)

        return value

    def get_str(self, key: str) -> str:
        """Converts a value(bytes) from redis to str """
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """Converts a value(bytes) from redis to int """
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
