"""Cobertura de skills por workspace declarado en openclaw.json."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from app.security import allowed_path
from app.services.openclaw_loader import load_openclaw_agents
from app.services.paths import repo_root

_AGENTS_TAIL = re.compile(r"agents/[^/]+$", re.IGNORECASE)


def _resolve_agent_dir(ws: str, root: Path) -> tuple[Path | None, str | None]:
    """
    Resuelve el directorio del agente (carpeta con skills/) desde workspace.
    Acepta ./agents/..., rutas absolutas bajo repo, o absolutas fuera del repo
    (re-basadas a repo_root/agents/<último segmento> si existe).
    Retorna (path, nota_diagnóstico); nota solo si no hubo directorio válido.
    """
    ws = (ws or "").strip().replace("\\", "/")
    if not ws:
        return None, None
    roots = (root.resolve(),)
    candidates: list[Path] = []

    if ws.startswith("./agents/"):
        candidates.append((root / ws[2:]).resolve())
    else:
        p = Path(ws).expanduser()
        try:
            pr = p.resolve()
        except OSError:
            pr = p
        candidates.append(pr)
        m = _AGENTS_TAIL.search(str(pr).replace("\\", "/"))
        if m:
            tail = m.group(0).replace("\\", "/")
            candidates.append((root / tail).resolve())

    seen: set[str] = set()
    for d in candidates:
        key = str(d)
        if key in seen:
            continue
        seen.add(key)
        try:
            r = d.resolve()
        except OSError:
            continue
        if r.is_dir() and allowed_path(r, roots):
            return r, None
    return None, "workspace_not_found"


def _count_skills(agent_dir: Path) -> tuple[int, list[str]]:
    sk = agent_dir / "skills"
    if not sk.is_dir():
        return 0, []
    slugs: list[str] = []
    for p in sorted(sk.glob("*/SKILL.md")):
        if p.is_file():
            slugs.append(p.parent.name)
    return len(slugs), slugs


def build_skills_coverage() -> dict[str, Any]:
    data = load_openclaw_agents()
    cfg = data.get("config") or {}
    lst = (cfg.get("agents") or {}).get("list") if isinstance(cfg.get("agents"), dict) else []
    if not isinstance(lst, list):
        lst = []
    root = repo_root().resolve()

    # Primera pasada: resolver dir + skills por workspace único
    cache: dict[str, tuple[int, list[str], str]] = {}
    for a in lst:
        if not isinstance(a, dict):
            continue
        ws = str(a.get("workspace") or "").strip()
        if not ws:
            continue
        agent_dir, _note = _resolve_agent_dir(ws, root)
        if agent_dir is None:
            continue
        try:
            rk = str(agent_dir.resolve().relative_to(root)).replace("\\", "/")
        except ValueError:
            rk = str(agent_dir)
        if rk not in cache:
            n, slugs = _count_skills(agent_dir)
            cache[rk] = (n, slugs, ws)

    rows: list[dict[str, Any]] = []
    for a in lst:
        if not isinstance(a, dict):
            continue
        aid = str(a.get("id") or a.get("agentId") or "")
        ws = str(a.get("workspace") or "").strip()
        if not aid:
            continue
        agent_dir, note = _resolve_agent_dir(ws, root)
        skill_count = 0
        resolved_key = ""
        if agent_dir is not None:
            try:
                resolved_key = str(agent_dir.resolve().relative_to(root)).replace("\\", "/")
            except ValueError:
                resolved_key = str(agent_dir)
            skill_count = cache.get(resolved_key, (0, [], ws))[0]
        rows.append(
            {
                "agent_id": aid,
                "workspace": ws,
                "skill_md_count": skill_count,
                "resolved_workspace": resolved_key or None,
                "workspace_note": note,
                "shared_workspace": False,
            }
        )

    by_resolved: dict[str, list[str]] = {}
    for r in rows:
        rk = r.get("resolved_workspace") or ""
        if rk:
            by_resolved.setdefault(rk, []).append(r["agent_id"])
    shared_keys = {k for k, ids in by_resolved.items() if len(set(ids)) > 1}
    for r in rows:
        rk = r.get("resolved_workspace") or ""
        r["shared_workspace"] = rk in shared_keys

    by_workspace: list[dict[str, Any]] = []
    for rk, (n, slugs, display_ws) in cache.items():
        ids = by_resolved.get(rk, [])
        by_workspace.append(
            {
                "workspace": rk,
                "display_path": display_ws,
                "agent_ids": sorted(set(ids)),
                "skill_md_count": n,
                "skill_slugs": slugs,
            }
        )
    by_workspace.sort(key=lambda x: x["workspace"])

    missing = [r for r in rows if r["skill_md_count"] == 0 and r["workspace"]]
    return {
        "agents": rows,
        "by_workspace": by_workspace,
        "without_skills": missing,
        "total_agents": len(rows),
    }
