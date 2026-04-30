"""Agentes en openclaw.json sin bloque heartbeat."""

from __future__ import annotations

from typing import Any

from app.services.openclaw_loader import load_openclaw_agents


def build_heartbeats_coverage() -> dict[str, Any]:
    data = load_openclaw_agents()
    cfg = data.get("config") or {}
    agents = (cfg.get("agents") or {}) if isinstance(cfg.get("agents"), dict) else {}
    lst = agents.get("list") if isinstance(agents.get("list"), list) else []
    rows: list[dict[str, Any]] = []
    missing: list[str] = []
    for a in lst:
        if not isinstance(a, dict):
            continue
        aid = str(a.get("id") or a.get("agentId") or "")
        if not aid:
            continue
        hb = a.get("heartbeat")
        has = isinstance(hb, dict) and bool(hb)
        rows.append({"agent_id": aid, "has_heartbeat": has})
        if not has:
            missing.append(aid)
    return {"agents": rows, "missing_heartbeat": missing, "total": len(rows)}
