import time
from collections import OrderedDict
from typing import Any, Optional

from .types import TTL


class LRUCache(OrderedDict):
    def __init__(self, maxsize: Optional[int] = None, *args, **kwargs):
        # Negative maxsize is treated as 0
        if maxsize and maxsize < 0:
            maxsize = 0
        self.maxsize = maxsize
        super().__init__(*args, **kwargs)

    def __getitem__(self, key: Any) -> Any:
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value

    def __setitem__(self, key: Any, value: Any):
        super().__setitem__(key, value)
        if self.maxsize and len(self) > self.maxsize:
            oldest = next(iter(self))
            del self[oldest]


class TTLCache(LRUCache):
    def __init__(self, ttl: Optional[TTL] = None, maxsize: Optional[int] = None):
        super().__init__(maxsize=maxsize)
        self.ttl = ttl

    def __contains__(self, key: Any) -> bool:
        if key not in self.keys():
            return False
        else:
            # Check if the key is expired, if true then delete the key and return False
            expired_at: float = super().__getitem__(key)[1]
            if expired_at and expired_at < time.time():
                del self[key]
                return False
            else:
                return True

    def __getitem__(self, key: Any) -> Any:
        value = super().__getitem__(key)[0]
        return value

    def __setitem__(self, key: Any, value: Any):
        expired_at = (time.time() + self.ttl) if self.ttl else None
        super().__setitem__(key, (value, expired_at))
