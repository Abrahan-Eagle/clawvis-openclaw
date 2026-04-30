"""Métricas del host (CPU, RAM, disco, red) con cache corto."""

from __future__ import annotations

import os
import threading
import time
from typing import Any

import psutil

_CACHE_LOCK = threading.Lock()
_CACHE: tuple[float, dict[str, Any]] | None = None
_TTL_SEC = 2.0


def get_system_metrics() -> dict[str, Any]:
    """Snapshot psutil; cache ~2s para no martillar el host."""
    now = time.monotonic()
    with _CACHE_LOCK:
        global _CACHE
        if _CACHE is not None and now - _CACHE[0] < _TTL_SEC:
            return _CACHE[1]

    cpu_percent = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    try:
        load_avg = list(os.getloadavg())
    except (AttributeError, OSError):
        load_avg = [0.0, 0.0, 0.0]
    disks: list[dict[str, Any]] = []
    for part in psutil.disk_partitions(all=False):
        try:
            u = psutil.disk_usage(part.mountpoint)
            disks.append(
                {
                    "mountpoint": part.mountpoint,
                    "fstype": part.fstype,
                    "used": u.used,
                    "total": u.total,
                    "percent": round(u.percent, 2),
                }
            )
        except OSError:
            continue
    disks = sorted(disks, key=lambda d: d["total"], reverse=True)[:8]
    net = psutil.net_io_counters()
    boot = psutil.boot_time()
    uptime_sec = max(0, int(time.time() - boot))

    snap: dict[str, Any] = {
        "cpu_percent": round(float(cpu_percent), 2),
        "load_avg": load_avg,
        "mem": {
            "used": mem.used,
            "total": mem.total,
            "percent": round(mem.percent, 2),
        },
        "disk": disks,
        "net": {
            "bytes_sent": net.bytes_sent,
            "bytes_recv": net.bytes_recv,
        },
        "uptime_sec": uptime_sec,
    }
    with _CACHE_LOCK:
        _CACHE = (now, snap)
    return snap
