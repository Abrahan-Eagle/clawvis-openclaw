"""Lectura de state/tasks y state/handoffs."""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from app.security import allowed_path
from app.services.paths import handoffs_dir, tasks_dir
from app.services.read_capped import read_capped_text
from app.services.state_cache import dir_mtime, get_cached

# Solo IDs de fichero seguros (evita path traversal en tasks_dir / f"{id}.json").
_TASK_ID_SAFE = re.compile(r"^[A-Za-z0-9._-]+$")


def _parse_started_ts(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        t = str(s).strip()
        if t.endswith("Z"):
            t = t[:-1] + "+00:00"
        return datetime.fromisoformat(t)
    except ValueError:
        return None


def _jmc_status(raw: dict[str, Any]) -> str:
    explicit = raw.get("status") or raw.get("task_status")
    if explicit in ("waiting_for_user", "open", "closed"):
        return explicit
    s = str(raw.get("status") or "")
    if s == "done":
        return "closed"
    if s == "blocked":
        return "waiting_for_user"
    if s in ("in_progress", ""):
        return "open"
    return "open"


def _load_tasks_impl() -> list[dict[str, Any]]:
    d = tasks_dir()
    if not d.is_dir():
        return []
    out: list[dict[str, Any]] = []
    roots = (d.resolve(),)
    for p in sorted(d.glob("*.json")):
        if not allowed_path(p, roots):
            continue
        text = read_capped_text(p)
        if text is None:
            continue
        try:
            raw = json.loads(text)
        except json.JSONDecodeError:
            continue
        raw = dict(raw)
        raw["_file"] = p.name
        raw["jmc_status"] = _jmc_status(raw)
        out.append(raw)

    def sort_key(x: dict[str, Any]) -> str:
        return str(x.get("started_at") or x.get("id") or "")

    out.sort(key=sort_key, reverse=True)
    return out


def load_tasks() -> list[dict[str, Any]]:
    d = tasks_dir()
    return get_cached("state_tasks", dir_mtime(d), _load_tasks_impl)


def _load_handoffs_impl() -> list[dict[str, Any]]:
    d = handoffs_dir()
    if not d.is_dir():
        return []
    out: list[dict[str, Any]] = []
    roots = (d.resolve(),)
    for p in sorted(d.glob("*.json")):
        if not allowed_path(p, roots):
            continue
        text = read_capped_text(p)
        if text is None:
            continue
        try:
            raw = json.loads(text)
        except json.JSONDecodeError:
            continue
        raw["_file"] = p.name
        out.append(raw)
    return out


def load_handoffs() -> list[dict[str, Any]]:
    d = handoffs_dir()
    return get_cached("state_handoffs", dir_mtime(d), _load_handoffs_impl)


def load_task_by_id(task_id: str) -> dict[str, Any] | None:
    tid = str(task_id or "").strip()
    if not tid or not _TASK_ID_SAFE.fullmatch(tid):
        return None
    base = tasks_dir().resolve()
    p = (tasks_dir() / f"{tid}.json").resolve()
    try:
        p.relative_to(base)
    except ValueError:
        return None
    if not p.is_file():
        return None
    text = read_capped_text(p)
    if text is None:
        return None
    try:
        raw = json.loads(text)
    except json.JSONDecodeError:
        return None
    raw = dict(raw)
    raw["_file"] = p.name
    raw["jmc_status"] = _jmc_status(raw)
    return raw


def handoffs_for_task_id(task_id: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for h in load_handoffs():
        tid = str(h.get("task_id") or h.get("taskId") or "")
        if tid == task_id:
            out.append(h)
    return out


def load_escalations() -> list[dict[str, Any]]:
    esc: list[dict[str, Any]] = []
    for t in load_tasks():
        if t.get("jmc_status") == "waiting_for_user" or str(t.get("status")) == "blocked":
            esc.append(t)
    return esc


def load_pending_approval_handoffs() -> list[dict[str, Any]]:
    """Handoffs con payload.approval.status == pending (AG-12, etc.)."""
    items: list[dict[str, Any]] = []
    for h in load_handoffs():
        payload = h.get("payload") if isinstance(h.get("payload"), dict) else {}
        appr = payload.get("approval") if isinstance(payload.get("approval"), dict) else {}
        if str(appr.get("status") or "").lower() != "pending":
            continue
        ch = payload.get("channels")
        channels = ch if isinstance(ch, list) else []
        items.append(
            {
                "handoff_id": h.get("id"),
                "_file": h.get("_file"),
                "task_id": h.get("task_id"),
                "dossier_id": h.get("dossier_id"),
                "schema": h.get("schema"),
                "from": h.get("from"),
                "to": h.get("to"),
                "ag": appr.get("ag"),
                "status": appr.get("status"),
                "channels": channels,
            }
        )
    return items


def aggregate_by_dossier(dossier_id: str, events_for_dossier_fn) -> dict[str, Any]:
    """Agrega tasks, handoffs y eventos por dossier_id.

    events_for_dossier_fn(path, did, limit=50) -> tuple[list[dict], bool] (eventos, truncado).
    """
    from app.services.paths import activity_log_path

    did = str(dossier_id)
    tasks = [t for t in load_tasks() if str(t.get("dossier_id") or "") == did]
    hands = [h for h in load_handoffs() if str(h.get("dossier_id") or "") == did]
    log = activity_log_path()
    evs, ev_trunc = events_for_dossier_fn(log, did, limit=50)
    tasks_open = sum(1 for t in tasks if t.get("jmc_status") == "open")
    tasks_closed = sum(1 for t in tasks if t.get("jmc_status") == "closed")
    handoffs_pending = sum(
        1 for h in hands if h.get("accepted_at") is None and h.get("rejected_at") is None
    )
    last_ts = ""
    if evs:
        last_ts = max(str(e.get("ts") or "") for e in evs)
    return {
        "dossier_id": did,
        "tasks": tasks,
        "handoffs": hands,
        "events": evs,
        "metrics": {
            "tasks_open": tasks_open,
            "tasks_closed": tasks_closed,
            "handoffs_pending": handoffs_pending,
            "last_event_ts": last_ts or None,
            "events_truncated": ev_trunc,
        },
    }


def aggregate_tag_counts(tasks: list[dict[str, Any]]) -> dict[str, int]:
    """Cuenta tareas por tag (tags[] en JSON de tarea)."""
    counts: dict[str, int] = {}
    for t in tasks:
        tags = t.get("tags")
        if not isinstance(tags, list):
            continue
        for tag in tags:
            s = str(tag).strip()
            if s:
                counts[s] = counts.get(s, 0) + 1
    return counts


def compute_state_summary() -> dict[str, Any]:
    """Contadores globales para sidebar / overview."""
    tasks = load_tasks()
    tag_counts = aggregate_tag_counts(tasks)
    open_tasks = sum(1 for t in tasks if t.get("jmc_status") == "open")
    waiting_user = sum(1 for t in tasks if t.get("jmc_status") == "waiting_for_user")
    now = datetime.now(timezone.utc)
    day = timedelta(days=1)
    stalled_tasks = 0
    for t in tasks:
        if t.get("jmc_status") != "open":
            continue
        ts = _parse_started_ts(str(t.get("started_at") or ""))
        if ts is None:
            continue
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        if now - ts > day:
            stalled_tasks += 1
    hands = load_handoffs()
    open_handoffs = sum(1 for h in hands if h.get("accepted_at") is None and h.get("rejected_at") is None)
    pending_approvals = len(load_pending_approval_handoffs())
    return {
        "open_tasks": open_tasks,
        "waiting_user": waiting_user,
        "stalled_tasks": stalled_tasks,
        "open_handoffs": open_handoffs,
        "pending_approvals": pending_approvals,
        "tag_counts": tag_counts,
    }


def task_ids_with_pending_ag_handoff() -> set[str]:
    """task_ids que tienen al menos un handoff con approval.pending."""
    out: set[str] = set()
    for h in load_pending_approval_handoffs():
        tid = str(h.get("task_id") or "")
        if tid:
            out.add(tid)
    return out
