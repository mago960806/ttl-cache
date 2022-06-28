import asyncio
import random
import time
import uuid
import pytest

from ttl_cache import ttl_cache, TTL


@ttl_cache(ttl=3, maxsize=128)
def task(wait: int):
    time.sleep(wait)


@ttl_cache(ttl=3, maxsize=128)
async def async_task(wait: int):
    await asyncio.sleep(wait)


@ttl_cache(ttl=0.1)
async def foo(a) -> tuple[uuid.UUID, TTL]:
    await asyncio.sleep(0.1)
    return uuid.uuid1(), 0.1


def test_sync_func():
    for wait in random.sample(range(1, 5), 3):
        # when cache miss
        t1 = time.time()
        task(wait)
        t2 = time.time()
        # when cache hit
        task(wait)
        t3 = time.time()
        # when cache key is expired
        time.sleep(3)
        t4 = time.time()
        task(wait)
        t5 = time.time()
        assert t2 - t1 > wait
        assert t3 - t2 < wait
        assert t5 - t4 > wait


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
        # when cache key is expired
        time.sleep(3)
        t4 = time.time()
        await async_task(wait)
        t5 = time.time()
        assert t2 - t1 > wait
        assert t3 - t2 < wait
        assert t5 - t4 > wait


@pytest.mark.asyncio
async def test_async_foo():
    foo1 = await foo(0)
    foo2 = await foo(0)
    assert foo1 == foo2

    await asyncio.sleep(0.1)
    foo3 = await foo(0)
    assert foo3 != foo2
