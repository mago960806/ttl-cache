import asyncio
import random
import time
import pytest

from ttl_cache import lru_cache


@lru_cache(maxsize=128)
def task(wait: int):
    time.sleep(wait)


@lru_cache(maxsize=128)
async def async_task(wait: int):
    await asyncio.sleep(wait)


def test_sync_func():
    for wait in random.sample(range(1, 5), 3):
        # when cache miss
        t1 = time.time()
        task(wait)
        t2 = time.time()
        # when cache hit
        task(wait)
        t3 = time.time()
        assert t2 - t1 > wait
        assert t3 - t2 < wait


@pytest.mark.asyncio
async def test_async_func():
    for wait in random.sample(range(1, 5), 3):
        # when cache miss
        t1 = time.time()
        await async_task(wait)
        t2 = time.time()
        # when cache hit
        await async_task(wait)
        t3 = time.time()
        assert t2 - t1 > wait
        assert t3 - t2 < wait
