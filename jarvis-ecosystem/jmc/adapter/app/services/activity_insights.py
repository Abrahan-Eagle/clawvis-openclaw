"""Una pasada sobre activity-log.jsonl: stats por agente, zombies, latencias start→end."""

from __future__ import annotations

import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from app.services.jsonl_reader import _parse_event_ts, load_activity_events_cached
from app.services.state_store import load_tasks

_SCAN_TTL = 5.0
_scan_cache: dict[str, tuple[float, dict[str, Any]]] = {}


def _cached_scan(path: Path) -> dict[str, Any]:
    key = str(path.resolve())
    now = time.monotonic()
    hit = _scan_cache.get(key)
    if hit and now - hit[0] < _SCAN_TTL:
        return hit[1]
    data = scan_activity_log(path)
    _scan_cache[key] = (now, data)
    return data


def _norm_type(ev: dict[str, Any]) -> str:
    return str(ev.get("type") or ev.get("kind") or "").lower()


def _is_error_type(t: str) -> bool:
    return t in ("block", "dossier-warn", "error", "fail") or "error" in t or "fail" in t


def scan_activity_log(path: Path) -> dict[str, Any]:
    """Escaneo completo del JSONL (mismo patrón que aggregate_last30days)."""
    now = datetime.now(timezone.utc)
    t24 = now - timedelta(hours=24)
    t7 = now - timedelta(days=7)

    agents_events_24h: Counter[str] = Counter()
    agents_events_7d: Counter[str] = Counter()
    agents_errors_24h: Counter[str] = Counter()
    agents_errors_7d: Counter[str] = Counter()

    last_ts_by_task: dict[str, datetime] = {}
    task_agent: dict[str, str] = defaultdict(lambda: "")
    task_first_start: dict[str, datetime] = {}
    task_last_end: dict[str, datetime] = {}
    dossier_by_task: dict[str, str] = {}

    latency_sum_by_agent: dict[str, float] = defaultdict(float)
    latency_count_by_agent: dict[str, int] = defaultdict(int)
    latency_sum_by_dossier: dict[str, float] = defaultdict(float)
    latency_count_by_dossier: dict[str, int] = defaultdict(int)

    for ev in load_activity_events_cached(path):
        ts = _parse_event_ts(str(ev.get("ts") or ""))
        if ts is None:
            continue
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)

        ag = str(ev.get("agent") or "").strip() or "unknown"
        tid = str(ev.get("task_id") or "").strip()
        did = str(ev.get("dossier_id") or "").strip()

        if tid:
            if ag:
                task_agent[tid] = ag
            prev = last_ts_by_task.get(tid)
            if prev is None or ts > prev:
                last_ts_by_task[tid] = ts

        typ = _norm_type(ev)
        if ts >= t24:
            agents_events_24h[ag] += 1
            if _is_error_type(typ):
                agents_errors_24h[ag] += 1
        if ts >= t7:
            agents_events_7d[ag] += 1
            if _is_error_type(typ):
                agents_errors_7d[ag] += 1

        if tid:
            if typ == "start":
                cur = task_first_start.get(tid)
                if cur is None or ts < cur:
                    task_first_start[tid] = ts
            elif typ == "end":
                cur = task_last_end.get(tid)
                if cur is None or ts > cur:
                    task_last_end[tid] = ts
            did_ev = str(ev.get("dossier_id") or "").strip()
            if did_ev:
                dossier_by_task[tid] = did_ev

    for tid, end_ts in task_last_end.items():
        st = task_first_start.get(tid)
        if st is None or end_ts <= st:
            continue
        sec = (end_ts - st).total_seconds()
        ag = task_agent.get(tid, "") or "unknown"
        latency_sum_by_agent[ag] += sec
        latency_count_by_agent[ag] += 1
        did = dossier_by_task.get(tid, "")
        if did:
            latency_sum_by_dossier[did] += sec
            latency_count_by_dossier[did] += 1

    top24 = [{"agent": a, "events": c} for a, c in agents_events_24h.most_common(20)]
    top7 = [{"agent": a, "events": c} for a, c in agents_events_7d.most_common(20)]
    err24 = [{"agent": a, "errors": c} for a, c in agents_errors_24h.most_common(20)]

    lat_ag = []
    for ag, s in latency_sum_by_agent.items():
        n = latency_count_by_agent[ag]
        if n:
            lat_ag.append({"agent": ag, "avg_sec": round(s / n, 2), "samples": n})

    lat_do = []
    for d, s in latency_sum_by_dossier.items():
        n = latency_count_by_dossier[d]
        if n:
            lat_do.append({"dossier_id": d, "avg_sec": round(s / n, 2), "samples": n})

    return {
        "top_agents_24h": top24,
        "top_agents_7d": top7,
        "top_errors_24h": err24,
        "last_ts_by_task": {k: v.isoformat().replace("+00:00", "Z") for k, v in last_ts_by_task.items()},
        "latency_by_agent": sorted(lat_ag, key=lambda x: -x["samples"])[:30],
        "latency_by_dossier": sorted(lat_do, key=lambda x: -x["samples"])[:30],
    }


def compute_agents_stats(path: Path) -> dict[str, Any]:
    s = _cached_scan(path)
    return {
        "window_hours_24": 24,
        "window_days_7": 7,
        "top_agents_24h": s["top_agents_24h"],
        "top_agents_7d": s["top_agents_7d"],
        "top_errors_24h": s["top_errors_24h"],
    }


def compute_zombies(path: Path, hours: float) -> dict[str, Any]:
    hours = max(1.0, min(float(hours), 720.0))
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    s = _cached_scan(path)
    last_map: dict[str, datetime] = {}
    for k, iso in s["last_ts_by_task"].items():
        try:
            t = datetime.fromisoformat(iso.replace("Z", "+00:00"))
            last_map[k] = t
        except ValueError:
            continue

    zombies = []
    for t in load_tasks():
        if str(t.get("jmc_status") or "") != "open":
            continue
        tid = str(t.get("id") or "").strip()
        if not tid:
            continue
        last = last_map.get(tid)
        if last is None:
            zombies.append({"task_id": tid, "reason": "no_events", "owner": t.get("owner")})
        elif last < cutoff:
            zombies.append(
                {
                    "task_id": tid,
                    "reason": "stale",
                    "owner": t.get("owner"),
                    "last_event_ts": last.isoformat().replace("+00:00", "Z"),
                }
            )
    return {"threshold_hours": hours, "items": zombies, "count": len(zombies)}


def compute_latency(path: Path) -> dict[str, Any]:
    s = _cached_scan(path)
    return {"by_agent": s["latency_by_agent"], "by_dossier": s["latency_by_dossier"]}
