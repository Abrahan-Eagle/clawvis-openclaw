"""Caché corta (TTL + mtime) para lecturas repetidas de state/tasks y state/handoffs."""

from __future__ import annotations

import os
import threading
import time
from pathlib import Path
from typing import Any, Callable, TypeVar

T = TypeVar("T")

_ttl = float((os.environ.get("JMC_STATE_CACHE_TTL") or "4").strip() or "4")
STATE_CACHE_TTL_SEC = max(1.0, min(_ttl, 30.0))

_store: dict[str, tuple[float, float, Any]] = {}
_store_lock = threading.Lock()


def dir_mtime(path: Path) -> float:
    """mtime del directorio; 0 si no existe o error."""
    try:
        if not path.is_dir():
            return 0.0
        return float(path.stat().st_mtime)
    except OSError:
        return 0.0


def get_cached(key: str, dep_mtime: float, loader: Callable[[], T]) -> T:
    """Devuelve `loader()` cacheado mientras TTL no expire y `dep_mtime` coincida."""
    now = time.monotonic()
    with _store_lock:
        hit = _store.get(key)
        if hit is not None:
            mono_ts, cached_mtime, val = hit
            if now - mono_ts < STATE_CACHE_TTL_SEC and cached_mtime == dep_mtime:
                return val  # type: ignore[return-value]
        val = loader()
        _store[key] = (now, dep_mtime, val)
        return val
