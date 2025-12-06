"""
Smart Caching Layer - Intelligent response and result caching
"""

import hashlib
import json
import time
from typing import Optional, Dict, Any
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class CacheEntry:
    """Represents a cached item"""
    key: str
    value: Any
    timestamp: float
    ttl: float  # Time to live in seconds
    hits: int = 0
    metadata: Dict = None

    def is_expired(self) -> bool:
        """Check if cache entry has expired"""
        if self.ttl == 0:  # 0 means no expiration
            return False
        return time.time() - self.timestamp > self.ttl

    def to_dict(self):
        return asdict(self)


class SmartCache:
    """
    Intelligent caching system for Agent Zero

    Features:
    - LLM response caching (semantic similarity)
    - Tool result caching
    - Embedding caching
    - Prompt template caching
    - Automatic cache invalidation
    - Cache statistics
    """

    def __init__(self, cache_dir: str = "work_dir/.cache", max_size_mb: int = 100):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.memory_cache: Dict[str, CacheEntry] = {}

        # Load persistent cache
        self._load_persistent_cache()

        # Statistics
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "total_requests": 0
        }

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        self.stats["total_requests"] += 1

        # Check memory cache first
        if key in self.memory_cache:
            entry = self.memory_cache[key]

            # Check if expired
            if entry.is_expired():
                del self.memory_cache[key]
                self.stats["misses"] += 1
                return None

            # Update hit count
            entry.hits += 1
            self.stats["hits"] += 1
            return entry.value

        # Check persistent cache
        value = self._get_from_disk(key)
        if value is not None:
            self.stats["hits"] += 1
            return value

        self.stats["misses"] += 1
        return None

    def set(self, key: str, value: Any, ttl: float = 3600, metadata: Dict = None):
        """Set value in cache"""

        entry = CacheEntry(
            key=key,
            value=value,
            timestamp=time.time(),
            ttl=ttl,
            metadata=metadata or {}
        )

        # Add to memory cache
        self.memory_cache[key] = entry

        # Persist to disk if large enough
        if self._should_persist(value):
            self._save_to_disk(entry)

        # Check cache size and evict if necessary
        self._check_cache_size()

    def delete(self, key: str):
        """Delete from cache"""
        if key in self.memory_cache:
            del self.memory_cache[key]

        # Also delete from disk
        cache_file = self._get_cache_file_path(key)
        if cache_file.exists():
            cache_file.unlink()

    def clear(self):
        """Clear entire cache"""
        self.memory_cache.clear()

        # Clear disk cache
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()

        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "total_requests": 0
        }

    def get_semantic(self, prompt: str, similarity_threshold: float = 0.9) -> Optional[Any]:
        """
        Get cached response based on semantic similarity of prompts
        Uses simple string similarity for now, could be upgraded to embeddings
        """

        best_match = None
        best_similarity = 0.0

        for entry in self.memory_cache.values():
            if entry.metadata and "prompt" in entry.metadata:
                cached_prompt = entry.metadata["prompt"]
                similarity = self._calculate_similarity(prompt, cached_prompt)

                if similarity > best_similarity and similarity >= similarity_threshold:
                    best_similarity = similarity
                    best_match = entry

        if best_match and not best_match.is_expired():
            best_match.hits += 1
            self.stats["hits"] += 1
            return best_match.value

        self.stats["misses"] += 1
        return None

    def cache_llm_response(self, prompt: str, response: str, model: str,
                          ttl: float = 3600):
        """Cache LLM response with semantic search support"""
        key = self._generate_key(f"llm:{model}:{prompt}")

        self.set(
            key=key,
            value=response,
            ttl=ttl,
            metadata={
                "type": "llm_response",
                "prompt": prompt,
                "model": model
            }
        )

    def cache_tool_result(self, tool_name: str, args: Dict, result: Any,
                         ttl: float = 1800):
        """Cache tool execution result"""
        # Create deterministic key from tool name and args
        args_str = json.dumps(args, sort_keys=True)
        key = self._generate_key(f"tool:{tool_name}:{args_str}")

        self.set(
            key=key,
            value=result,
            ttl=ttl,
            metadata={
                "type": "tool_result",
                "tool": tool_name,
                "args": args
            }
        )

    def cache_embedding(self, text: str, embedding: list, model: str, ttl: float = 0):
        """Cache text embedding (no expiration by default)"""
        key = self._generate_key(f"embedding:{model}:{text}")

        self.set(
            key=key,
            value=embedding,
            ttl=ttl,
            metadata={
                "type": "embedding",
                "model": model,
                "text_length": len(text)
            }
        )

    def get_stats(self) -> Dict:
        """Get cache statistics"""
        hit_rate = (self.stats["hits"] / self.stats["total_requests"] * 100
                   if self.stats["total_requests"] > 0 else 0)

        return {
            **self.stats,
            "hit_rate_percent": round(hit_rate, 2),
            "memory_entries": len(self.memory_cache),
            "disk_entries": len(list(self.cache_dir.glob("*.json"))),
            "cache_size_mb": self._get_cache_size_mb()
        }

    def _generate_key(self, data: str) -> str:
        """Generate cache key from data"""
        return hashlib.sha256(data.encode()).hexdigest()

    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """
        Calculate similarity between two strings
        Uses Jaccard similarity on word sets
        Could be upgraded to use embeddings for better semantic matching
        """
        words1 = set(str1.lower().split())
        words2 = set(str2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union)

    def _should_persist(self, value: Any) -> bool:
        """Determine if value should be persisted to disk"""
        # Persist if value is large or important
        try:
            size = len(json.dumps(value))
            return size > 1024  # Persist if > 1KB
        except:
            return False

    def _save_to_disk(self, entry: CacheEntry):
        """Save cache entry to disk"""
        cache_file = self._get_cache_file_path(entry.key)

        try:
            with open(cache_file, 'w') as f:
                json.dump(entry.to_dict(), f)
        except Exception as e:
            print(f"Failed to save cache entry: {e}")

    def _get_from_disk(self, key: str) -> Optional[Any]:
        """Load cache entry from disk"""
        cache_file = self._get_cache_file_path(key)

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, 'r') as f:
                entry_data = json.load(f)

            entry = CacheEntry(**entry_data)

            if entry.is_expired():
                cache_file.unlink()
                return None

            # Load into memory cache
            self.memory_cache[key] = entry
            return entry.value

        except Exception as e:
            print(f"Failed to load cache entry: {e}")
            return None

    def _get_cache_file_path(self, key: str) -> Path:
        """Get path to cache file for key"""
        return self.cache_dir / f"{key}.json"

    def _load_persistent_cache(self):
        """Load persistent cache from disk"""
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r') as f:
                    entry_data = json.load(f)

                entry = CacheEntry(**entry_data)

                if not entry.is_expired():
                    self.memory_cache[entry.key] = entry
                else:
                    cache_file.unlink()

            except Exception as e:
                print(f"Failed to load cache file {cache_file}: {e}")

    def _check_cache_size(self):
        """Check cache size and evict if necessary"""
        current_size = self._get_cache_size_bytes()

        if current_size > self.max_size_bytes:
            # Evict least recently used entries
            sorted_entries = sorted(
                self.memory_cache.values(),
                key=lambda e: (e.hits, e.timestamp)
            )

            # Remove bottom 20% of entries
            num_to_remove = len(sorted_entries) // 5

            for entry in sorted_entries[:num_to_remove]:
                self.delete(entry.key)
                self.stats["evictions"] += 1

    def _get_cache_size_bytes(self) -> int:
        """Get total cache size in bytes"""
        total = 0

        for cache_file in self.cache_dir.glob("*.json"):
            total += cache_file.stat().st_size

        return total

    def _get_cache_size_mb(self) -> float:
        """Get cache size in MB"""
        return round(self._get_cache_size_bytes() / (1024 * 1024), 2)


# Global cache instance
_global_cache: Optional[SmartCache] = None


def get_cache() -> SmartCache:
    """Get global cache instance"""
    global _global_cache
    if _global_cache is None:
        _global_cache = SmartCache()
    return _global_cache
