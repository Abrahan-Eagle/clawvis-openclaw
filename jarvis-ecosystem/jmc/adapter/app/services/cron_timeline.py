"""Grilla semanal de ventanas activas (heartbeats) + heartbeats recientes en activity-log."""

from __future__ import annotations

from collections import deque
from datetime import datetime, timedelta, timezone
from typing import Any

from app.services.jsonl_reader import _parse_event_ts, load_activity_events_cached
from app.services.openclaw_loader import _within_active_hours, load_agent_heartbeats
from app.services.paths import activity_log_path


def build_cron_timeline(days: int = 7) -> dict[str, Any]:
    days = max(1, min(int(days), 14))
    hb = load_agent_heartbeats()
    items = hb.get("items") if isinstance(hb.get("items"), list) else []
    now_utc = datetime.now(timezone.utc)
    start = (now_utc - timedelta(days=days - 1)).replace(hour=0, minute=0, second=0, microsecond=0)

    hours_total = days * 24
    agents_grid: list[dict[str, Any]] = []
    for it in items:
        if not isinstance(it, dict):
            continue
        aid = str(it.get("id") or "")
        hb_stub = {"every": it.get("every"), "activeHours": it.get("activeHours") or {}}
        mask: list[bool] = []
        for i in range(hours_total):
            t = start + timedelta(hours=i)
            mask.append(_within_active_hours(hb_stub, t))
        agents_grid.append({"id": aid, "hours_active": mask})

    log = activity_log_path()
    dq: deque[dict[str, Any]] = deque(maxlen=80)
    cutoff = now_utc - timedelta(days=days)
    for ev in load_activity_events_cached(log):
        typ = str(ev.get("type") or ev.get("kind") or "").lower()
        if typ != "heartbeat":
            continue
        ts = _parse_event_ts(str(ev.get("ts") or ""))
        if ts is None:
            continue
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        if ts < cutoff:
            continue
        dq.append(
            {
                "ts": str(ev.get("ts") or ""),
                "agent": str(ev.get("agent") or ""),
                "type": typ,
            }
        )
    runs_recent = list(dq)

    return {
        "window_days": days,
        "grid_start_utc": start.isoformat().replace("+00:00", "Z"),
        "hours_total": hours_total,
        "agents": agents_grid,
        "runs_recent": runs_recent,
    }
