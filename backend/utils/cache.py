import hashlib
import json
import time
from typing import Optional, List
from backend.config import CACHE_TTL_SECONDS
from backend.models.response import Recommendation

class ResponseCache:
    def __init__(self, ttl: int = CACHE_TTL_SECONDS):
        self.ttl = ttl
        self._cache = {}

    def _hash_key(self, prefs: dict) -> str:
        # Normalize the dictionary keys and values for a consistent hash
        normalized = {k: str(v).strip().lower() for k, v in prefs.items()}
        serialized = json.dumps(normalized, sort_keys=True)
        return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

    def get(self, prefs: dict) -> Optional[List[Recommendation]]:
        key = self._hash_key(prefs)
        if key in self._cache:
            entry = self._cache[key]
            if time.time() - entry['timestamp'] <= self.ttl:
                return entry['data']
            else:
                del self._cache[key]
        return None

    def set(self, prefs: dict, recommendations: List[Recommendation]):
        # Prevent unbounded growth (simple LRU logic by dropping oldest if > 1000)
        if len(self._cache) >= 1000:
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k]['timestamp'])
            del self._cache[oldest_key]

        key = self._hash_key(prefs)
        self._cache[key] = {
            'timestamp': time.time(),
            'data': recommendations
        }

# Singleton instance
llm_cache = ResponseCache()
