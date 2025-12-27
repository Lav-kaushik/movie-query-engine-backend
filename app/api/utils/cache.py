import time 
from typing import Any

class LocalCache:
    def __init__(self):
        # key -> (expires at , details about the movie)
        self._store: dict[str , tuple[float , Any]] = {}

    def __is_expired(self , expiry: float) -> bool:
        return time.time() > expiry

    def set(self , key: str , value: Any , ttl_seconds: int):
        # store data in cache
        expiry_time = time.time() + ttl_seconds
        self._store[key] = (expiry_time , value)
    
    def get(self, key: str) -> Any | None:
        data = self._store.get(key)  

        if not data:
            return None

        expiry, value = data

        # delete expired data
        if self.__is_expired(expiry):
            del self._store[key]
            return None

        return value
    
    def clear(self):
        self._store.clear()

