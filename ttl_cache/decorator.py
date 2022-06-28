import asyncio
import asyncio as aio
import threading
from typing import Optional

from .cache import LRUCache, TTLCache
from .types import TTL
from .utils import make_key


def lru_cache(maxsize: Optional[int] = 128):
    cache = LRUCache(maxsize)

    def decorator(func):
        def wrapper(*args, **kwargs):
            key = make_key(args, kwargs)
            with threading.Lock():
                if key in cache:
                    return cache[key]
                else:
                    cache[key] = func(*args, **kwargs)
                    return cache[key]

        async def async_wrapper(*args, **kwargs):
            key = make_key(args, kwargs)
            async with asyncio.Lock():
                if key in cache:
                    return cache[key]
                else:
                    cache[key] = await func(*args, **kwargs)
                    return cache[key]

        if aio.iscoroutinefunction(func):
            return async_wrapper
        return wrapper

    return decorator


def ttl_cache(ttl: Optional[TTL] = 60, maxsize: Optional[int] = 1024):
    cache = TTLCache(ttl, maxsize)

    def decorator(func):
        def wrapper(*args, **kwargs):
            key = make_key(args, kwargs)
            with threading.Lock():
                if key in cache:
                    return cache[key]
                else:
                    cache[key] = func(*args, **kwargs)
                    return cache[key]

        async def async_wrapper(*args, **kwargs):
            key = make_key(args, kwargs)
            async with asyncio.Lock():
                if key in cache:
                    return cache[key]
                else:
                    cache[key] = await func(*args, **kwargs)
                    return cache[key]

        if aio.iscoroutinefunction(func):
            return async_wrapper
        return wrapper

    return decorator
