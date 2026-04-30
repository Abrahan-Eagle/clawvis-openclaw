"""Extensiones v1.10: CPU per-core, resumen de procesos, latencia stat."""

from __future__ import annotations

import logging
import time
from typing import Any

import psutil

from app.services.paths import state_dir

_log = logging.getLogger(__name__)


def get_cpu_detail() -> dict[str, Any]:
    vals = psutil.cpu_percent(interval=0.08, percpu=True)
    if not isinstance(vals, list):
        vals = [float(vals)]
    vals = [round(float(x), 2) for x in vals[:64]]
    return {"per_cpu_percent": vals, "count": len(vals)}


def get_proc_summary() -> dict[str, Any]:
    count = 0
    mem_total = 0
    for p in psutil.process_iter(attrs=["memory_info"]):
        count += 1
        if count > 400:
            break
        try:
            mi = p.info.get("memory_info")
            if mi and mi.rss:
                mem_total += int(mi.rss)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return {"processes_scanned": count, "rss_total_kb": mem_total // 1024}


def get_fs_latency() -> dict[str, Any]:
    p = state_dir()
    t0 = time.perf_counter()
    try:
        p.stat()
        dt_ms = (time.perf_counter() - t0) * 1000
        if dt_ms > 50:
            dt_ms = 50.0
        return {"path": str(p), "stat_ms": round(dt_ms, 3)}
    except OSError as e:
        _log.warning("fs-latency stat falló en %s: %s", p, e)
        return {"path": str(p), "stat_ms": None, "error": "stat_failed"}
