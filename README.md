# 介绍
参考 [functools.lru_cache](https://github.com/python/cpython/blob/3.10/Lib/functools.py) 实现的 `ttl_cache`装饰器

# 使用方法
可以装饰同步函数或异步函数，同时也支持装饰类方法

```python
import time
import asyncio


from ttl_cache import ttl_cache


@ttl_cache(ttl=3, maxsize=128)
def task(wait: int):
    time.sleep(wait)


@ttl_cache(ttl=3, maxsize=128)
async def async_task(wait: int):
    await asyncio.sleep(wait)

```

支持缓存绝大部分类型的参数，包括自定义对象、嵌套的字典、列表、元组、实现了`__dict__`方法的类等。