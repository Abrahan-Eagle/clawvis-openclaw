"""openclaw.json y skills (SKILL.md frontmatter)."""

from __future__ import annotations

import json
import logging
import re
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import yaml

from app.security import allowed_path, sanitize_obj
from app.services.automations_diff import load_yaml_preview, list_automation_yamls, run_sync_check
from app.services.jsonl_reader import _parse_event_ts, load_activity_events_cached
from app.services.paths import activity_log_path, openclaw_json_path, repo_root
from app.services.read_capped import read_capped_text

_log = logging.getLogger(__name__)


def _openclaw_source_rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root().resolve()))
    except ValueError:
        return path.name


def _parse_every_interval(s: str | None) -> timedelta | None:
    if not s:
        return None
    t = str(s).strip().lower()
    if t in ("0", "0m", "0h"):
        return None
    m = re.match(r"^(\d+)\s*(m|h|min|hour|hours)$", t)
    if not m:
        m = re.match(r"^(\d+)(m|h)$", t)
    if not m:
        return None
    n = int(m.group(1))
    unit = m.group(2)
    if unit in ("h", "hour", "hours"):
        return timedelta(hours=n)
    return timedelta(minutes=n)


def _parse_hhmm(s: str | None) -> tuple[int, int] | None:
    if not s:
        return None
    m = re.match(r"^(\d{1,2}):(\d{2})$", str(s).strip())
    if not m:
        return None
    h, mm = int(m.group(1)), int(m.group(2))
    if h > 24 or mm > 59 or (h == 24 and mm > 0):
        return None
    return h, mm


def _tz_from_active_hours(ah: dict[str, Any]):
    tzname = str(ah.get("timezone") or "UTC")
    try:
        return ZoneInfo(tzname)
    except ZoneInfoNotFoundError:
        return ZoneInfo("UTC")


def _active_window_for_local_date(day: date, tz: ZoneInfo, ah: dict[str, Any]) -> tuple[datetime, datetime] | None:
    """Ventana [start, end) en hora local; end 24:00 = medianoche del día siguiente."""
    start_s = _parse_hhmm(ah.get("start"))
    end_s = _parse_hhmm(ah.get("end"))
    if not start_s or not end_s:
        return None
    sh, sm = start_s
    eh, em = end_s
    if sh >= 24 or (sh == 24 and sm > 0):
        return None
    start_dt = datetime.combine(day, datetime.min.time().replace(hour=sh, minute=sm), tzinfo=tz)
    if eh == 24 and em == 0:
        end_dt = datetime.combine(day + timedelta(days=1), datetime.min.time(), tzinfo=tz)
    else:
        end_dt = datetime.combine(day, datetime.min.time().replace(hour=eh, minute=em), tzinfo=tz)
    return start_dt, end_dt


def _next_due_estimate(hb: dict[str, Any], now_utc: datetime) -> str | None:
    """ISO8601 UTC aproximado del próximo tick."""
    every = _parse_every_interval(str(hb.get("every") or ""))
    if not every:
        return None
    ah = hb.get("activeHours") if isinstance(hb.get("activeHours"), dict) else {}
    tz = _tz_from_active_hours(ah)
    now_local = now_utc.astimezone(tz)
    win = _active_window_for_local_date(now_local.date(), tz, ah)
    if not win:
        nxt = now_utc + every
        return nxt.isoformat().replace("+00:00", "Z")
    s0, e0 = win
    if now_local < s0:
        candidate = s0
    elif now_local >= e0:
        nd = now_local.date() + timedelta(days=1)
        win2 = _active_window_for_local_date(nd, tz, ah)
        candidate = win2[0] if win2 else now_local + every
    else:
        cand = now_local + every
        if cand < e0:
            candidate = cand
        else:
            nd = now_local.date() + timedelta(days=1)
            win2 = _active_window_for_local_date(nd, tz, ah)
            candidate = win2[0] if win2 else now_local + every
    return candidate.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _within_active_hours(hb: dict[str, Any], now_utc: datetime) -> bool:
    ah = hb.get("activeHours") if isinstance(hb.get("activeHours"), dict) else {}
    tz = _tz_from_active_hours(ah)
    nl = now_utc.astimezone(tz)
    w = _active_window_for_local_date(nl.date(), tz, ah)
    if not w:
        return True
    s0, e0 = w
    return s0 <= nl < e0


def load_agent_heartbeats() -> dict[str, Any]:
    """Extrae heartbeat por agente desde openclaw.json (agents.list[].heartbeat)."""
    data = load_openclaw_agents()
    cfg = data.get("config") or {}
    agents_block = cfg.get("agents") or {}
    lst = agents_block.get("list") if isinstance(agents_block.get("list"), list) else []
    items: list[dict[str, Any]] = []
    now_utc = datetime.now(timezone.utc)
    for a in lst:
        if not isinstance(a, dict):
            continue
        hb = a.get("heartbeat")
        if not isinstance(hb, dict):
            continue
        aid = str(a.get("id") or a.get("agentId") or "")
        ah = hb.get("activeHours") if isinstance(hb.get("activeHours"), dict) else {}
        items.append(
            {
                "id": aid,
                "every": hb.get("every"),
                "target": hb.get("target"),
                "lightContext": hb.get("lightContext"),
                "activeHours": ah,
                "next_due_estimate": _next_due_estimate(hb, now_utc),
                "within_active_hours": _within_active_hours(hb, now_utc),
            }
        )
    return {"source": data.get("source"), "items": items}


def load_openclaw_agents() -> dict[str, Any]:
    p = openclaw_json_path()
    src = _openclaw_source_rel(p)
    if not p.is_file():
        return {"source": src, "error": "missing", "agents": {"list": []}}
    text = read_capped_text(p)
    if text is None:
        return {"source": src, "error": "too_large", "agents": {"list": []}}
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        _log.warning("openclaw.json JSON inválido (%s): %s", src, e)
        return {"source": src, "error": "json_invalid", "agents": {"list": []}}
    agents_block = data.get("agents") or {}
    if isinstance(agents_block.get("list"), list):
        for a in agents_block["list"]:
            if not isinstance(a, dict):
                continue
            ui = a.get("ui") if isinstance(a.get("ui"), dict) else {}
            em = ui.get("emoji")
            co = ui.get("color")
            desc = ui.get("description")
            loc = ui.get("location")
            bd = ui.get("birth_date")
            if em is not None or co is not None or desc is not None or loc is not None or bd is not None:
                a["ui"] = {
                    "emoji": str(em or "")[:16],
                    "color": str(co or "")[:32],
                    "description": str(desc or "")[:400],
                    "location": str(loc or "")[:120],
                    "birth_date": str(bd or "")[:32],
                }
    return {"source": src, "config": sanitize_obj(data), "agents": data.get("agents", {})}


_FM_BOUND = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL | re.MULTILINE)


def _skill_frontmatter(path: Path) -> dict[str, Any]:
    text = read_capped_text(path)
    if text is None:
        return {}
    m = _FM_BOUND.match(text)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


def load_skills_map() -> dict[str, Any]:
    root = repo_root()
    roots = (root.resolve(),)
    by_workspace: dict[str, list[dict[str, Any]]] = {}
    collected: list[Path] = []
    collected.extend(root.glob("agents/*/skills/*/SKILL.md"))
    collected.extend(root.glob("skills/*/SKILL.md"))
    collected.extend(root.glob("skills/global/*/SKILL.md"))

    for path in sorted(set(collected)):
        if not path.is_file():
            continue
        if not allowed_path(path, roots):
            continue
        try:
            rel = path.relative_to(root)
        except ValueError:
            continue
        parts = rel.parts
        if parts[0] == "agents" and len(parts) >= 2:
            workspace = f"agents/{parts[1]}"
        elif parts[0] == "skills" and len(parts) >= 2 and parts[1] == "global":
            workspace = "skills/global"
        elif parts[0] == "skills":
            workspace = f"skills/{parts[1]}"
        else:
            workspace = parts[0]

        fm = _skill_frontmatter(path)
        entry = {
            "path": str(rel),
            "name": fm.get("name") or path.parent.name,
            "description": (str(fm.get("description") or ""))[:240],
        }
        by_workspace.setdefault(workspace, []).append(entry)

    return {"workspaces": by_workspace}


def load_gateway_runtime(window_hours: int = 24) -> dict[str, Any]:
    """Métricas de actividad reciente por agente (activity-log) cruzadas con agents.list de openclaw.json."""
    window_hours = max(1, min(168, int(window_hours)))
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=window_hours)

    pack = load_openclaw_agents()
    agents_block = pack.get("agents") if isinstance(pack.get("agents"), dict) else {}
    lst = agents_block.get("list") if isinstance(agents_block.get("list"), list) else []
    configured_ids: list[str] = []
    for a in lst:
        if isinstance(a, dict):
            aid = str(a.get("id") or a.get("agentId") or "").strip()
            if aid:
                configured_ids.append(aid)

    totals_by_kind: Counter[str] = Counter()
    total_events = 0
    per_agent_events: Counter[str] = Counter()
    per_agent_heartbeat: Counter[str] = Counter()

    for ev in load_activity_events_cached(activity_log_path()):
        ts = _parse_event_ts(str(ev.get("ts") or ""))
        if ts is None:
            continue
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        if ts < cutoff:
            continue
        typ = str(ev.get("type") or ev.get("kind") or "") or "unknown"
        ag = str(ev.get("agent") or "").strip() or "unknown"
        total_events += 1
        totals_by_kind[typ] += 1
        per_agent_events[ag] += 1
        if typ == "heartbeat":
            per_agent_heartbeat[ag] += 1

    agents_out: list[dict[str, Any]] = []
    for aid in configured_ids:
        evc = int(per_agent_events.get(aid, 0))
        hbc = int(per_agent_heartbeat.get(aid, 0))
        agents_out.append(
            {
                "id": aid,
                "events_24h": evc,
                "heartbeats_24h": hbc,
                "silent": evc == 0,
                "configured": True,
            }
        )

    by_kind_rows = [{"kind": k, "count": int(c)} for k, c in sorted(totals_by_kind.items())]
    return {
        "window_hours": window_hours,
        "totals": {
            "events_24h": total_events,
            "by_kind": by_kind_rows,
        },
        "agents": agents_out,
    }


def load_automations_bundle() -> dict[str, Any]:
    listing = list_automation_yamls()
    sync = run_sync_check()
    previews = load_yaml_preview()
    return {
        **listing,
        "sync_check": sync,
        "yaml_preview": previews,
    }
