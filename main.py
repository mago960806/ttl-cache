import asyncio as aio
import uuid

from ttl_cache import ttl_cache

TTL = int | float  # 过期时间 单位(秒)


async def test():
    cost = 0.1
    ttl = 0.1

    @ttl_cache(ttl)
    async def foo(a) -> tuple[uuid.UUID, TTL]:
        await aio.sleep(cost)
        return uuid.uuid1(), ttl

    task = aio.create_task(foo(0))

    assert await task == await foo(0)
    assert isinstance((await task)[0], uuid.UUID)

    await aio.sleep(ttl)
    assert await foo(0) != await task


if __name__ == "__main__":
    aio.run(test())
