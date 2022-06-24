一个异步函数的带有 ttl 缓存功能的装饰器

## Install 
```shell
pip install asyncio-ttl-cache
```

## Example
```python
import asyncio
from asyncio_ttl_cache import ttl_cache


@ttl_cache(ttl=3)
async def sum(a: int, b: int) -> int:
    await asyncio.sleep(1)
    return a + b

if __name__ == '__main__':
    asyncio.run(sum(1, 2))

```
