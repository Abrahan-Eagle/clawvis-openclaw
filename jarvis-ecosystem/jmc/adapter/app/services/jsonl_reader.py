"""Lectura acotada de JSONL (activity feed)."""

from __future__ import annotations

import json
import threading
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator

_ACTIVITY_CACHE_TTL = 5.0
_activity_events_cache: dict[str, tuple[float, float, list[dict[str, Any]]]] = {}
_activity_cache_lock = threading.Lock()

_MAX_READ = 8 * 1024 * 1024  # 8 MiB cap
_MAX_JSONL_LINE = 256 * 1024  # por línea (DoS RAM)
_MAX_MATCHING_EVENTS = 5000  # cap en RAM por task_id / dossier_id


def _activity_cursor(value: str | None) -> int:
    """Índice de paginación JSONL; inválido → 0."""
    if value is None or str(value).strip() == "":
        return 0
    try:
        n = int(str(value).strip(), 10)
    except (ValueError, TypeError):
        return 0
    return max(0, n)


def iter_activity_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    if not path.is_file():
        return
    with path.open(encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if len(line) > _MAX_JSONL_LINE:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def load_activity_events_cached(path: Path, *, ttl: float = _ACTIVITY_CACHE_TTL) -> list[dict[str, Any]]:
    """
    Lista completa de eventos parseados con caché en RAM (TTL + mtime del fichero).
    Usar donde ya se recorría todo el JSONL; evita N lecturas concurrentes del mismo archivo.
    """
    key = str(path.resolve())
    now = time.monotonic()
    try:
        mtime = float(path.stat().st_mtime) if path.is_file() else 0.0
    except OSError:
        mtime = 0.0
    with _activity_cache_lock:
        hit = _activity_events_cache.get(key)
        if hit is not None:
            mono_ts, cached_mtime, evs = hit
            if now - mono_ts < ttl and cached_mtime == mtime:
                return evs
        evs = list(iter_activity_jsonl(path))
        _activity_events_cache[key] = (now, mtime, evs)
        return evs


def scan_cached(path: Path, *, ttl: float = _ACTIVITY_CACHE_TTL) -> dict[str, Any]:
    """
    Misma caché que load_activity_events_cached + índices por task_id, dossier_id, agent y kind/type.
    Los valores son listas de referencias al mismo dict por evento (no copias profundas).
    """
    events = load_activity_events_cached(path, ttl=ttl)
    by_task_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_dossier_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_agent: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_kind: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for ev in events:
        tid = str(ev.get("task_id") or "").strip()
        if tid:
            by_task_id[tid].append(ev)
        did = str(ev.get("dossier_id") or "").strip()
        if did:
            by_dossier_id[did].append(ev)
        ag = str(ev.get("agent") or "").strip() or "unknown"
        by_agent[ag].append(ev)
        k = str(ev.get("type") or ev.get("kind") or "") or "unknown"
        by_kind[k].append(ev)
    return {
        "events": events,
        "by_task_id": dict(by_task_id),
        "by_dossier_id": dict(by_dossier_id),
        "by_agent": dict(by_agent),
        "by_kind": dict(by_kind),
    }


def events_for_task(path: Path, task_id: str) -> tuple[list[dict[str, Any]], bool]:
    """Devuelve eventos ordenados por ts y si la lista se truncó por límite de entradas."""
    tid = str(task_id)
    out: list[dict[str, Any]] = []
    total = 0
    for ev in iter_activity_jsonl(path):
        if str(ev.get("task_id") or "") == tid:
            total += 1
            out.append(ev)
            if len(out) > _MAX_MATCHING_EVENTS:
                out = out[-_MAX_MATCHING_EVENTS:]
    out.sort(key=lambda e: str(e.get("ts") or ""))
    truncated = total > _MAX_MATCHING_EVENTS
    return out, truncated


def events_for_dossier(path: Path, dossier_id: str, *, limit: int = 50) -> tuple[list[dict[str, Any]], bool]:
    """Últimos `limit` eventos por dossier_id (tras ordenar por ts); flag si hubo truncado."""
    did = str(dossier_id)
    out: list[dict[str, Any]] = []
    total = 0
    for ev in iter_activity_jsonl(path):
        if str(ev.get("dossier_id") or "") == did:
            total += 1
            out.append(ev)
            if len(out) > _MAX_MATCHING_EVENTS:
                out = out[-_MAX_MATCHING_EVENTS:]
    out.sort(key=lambda e: str(e.get("ts") or ""))
    lim = max(1, min(limit, 500))
    page = out[-lim:]
    truncated = total > _MAX_MATCHING_EVENTS or total > lim
    return page, truncated


def _parse_event_ts(ts: str) -> datetime | None:
    if not ts:
        return None
    try:
        s = str(ts).strip()
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def aggregate_last30days(path: Path) -> dict[str, Any]:
    """Agrega eventos últimos 30 días desde activity-log.jsonl."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    by_day: dict[str, dict[str, int]] = {}
    by_agent: Counter[str] = Counter()
    by_kind: Counter[str] = Counter()
    total = 0

    for ev in load_activity_events_cached(path):
        ts = _parse_event_ts(str(ev.get("ts") or ""))
        if ts is None:
            continue
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        if ts < cutoff:
            continue
        total += 1
        day = ts.strftime("%Y-%m-%d")
        by_day.setdefault(day, {"started": 0, "closed": 0, "events": 0})
        by_day[day]["events"] += 1
        typ = str(ev.get("type") or "")
        by_kind[typ or "unknown"] += 1
        ag = str(ev.get("agent") or "") or "unknown"
        by_agent[ag] += 1
        if typ == "start":
            by_day[day]["started"] += 1
        elif typ == "end":
            by_day[day]["closed"] += 1

    day_list = sorted(by_day.keys())
    by_day_rows = [
        {"date": d, **by_day[d]}
        for d in day_list
    ]
    top5 = [{"agent": a, "count": c} for a, c in by_agent.most_common(5)]
    kinds = [{"kind": k, "count": c} for k, c in sorted(by_kind.items(), key=lambda x: -x[1])[:20]]

    return {
        "window_days": 30,
        "total_events": total,
        "by_day": by_day_rows,
        "by_agent_top5": top5,
        "by_kind": kinds,
    }


def read_activity_tail(
    path: Path,
    *,
    limit: int = 50,
    cursor: str | None = None,
    since_iso: str | None = None,
    agent: str | None = None,
    event_type: str | None = None,
) -> dict[str, Any]:
    """Lee JSONL; para archivos grandes solo el tail. Paginación por índice cursor (string int)."""
    limit = max(1, min(limit, 500))
    start = _activity_cursor(cursor)

    if not path.is_file():
        return {"events": [], "next_cursor": None, "truncated": False}

    size = path.stat().st_size
    if size <= _MAX_READ:
        text = path.read_text(encoding="utf-8", errors="replace")
    else:
        with path.open("rb") as f:
            f.seek(max(0, size - 512 * 1024))
            raw = f.read()
        text = raw.decode("utf-8", errors="replace")
        if "\n" in text:
            text = text.split("\n", 1)[1]

    since_cutoff: datetime | None = None
    if since_iso and str(since_iso).strip():
        since_cutoff = _parse_event_ts(str(since_iso).strip())
        if since_cutoff is not None and since_cutoff.tzinfo is None:
            since_cutoff = since_cutoff.replace(tzinfo=timezone.utc)

    events: list[dict[str, Any]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if len(line) > _MAX_JSONL_LINE:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if since_cutoff is not None:
            ev_ts = _parse_event_ts(str(ev.get("ts") or ""))
            if ev_ts is None:
                continue
            if ev_ts.tzinfo is None:
                ev_ts = ev_ts.replace(tzinfo=timezone.utc)
            if ev_ts < since_cutoff:
                continue
        if agent and str(ev.get("agent") or "") != agent:
            continue
        if event_type:
            t = str(ev.get("type") or ev.get("kind") or "")
            if t != event_type:
                continue
        events.append(ev)

    page = events[start : start + limit]
    next_cursor = str(start + len(page)) if len(page) == limit and start + len(page) < len(events) else None
    if len(page) == limit and start + len(page) >= len(events):
        next_cursor = None

    return {
        "events": page,
        "next_cursor": next_cursor,
        "truncated": size > _MAX_READ,
        "total_filtered": len(events),
    }
