"""GET /v1/memory/* — listado y lectura de MEMORY.md / SOUL.md por agente (solo lectura)."""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query

from app.config import get_memory_stale_days
from app.security import allowed_path, require_token
from app.services.paths import repo_root
from app.services.read_capped import read_capped_text
from app.util_response import envelope

router = APIRouter(prefix="/memory", dependencies=[Depends(require_token)])

_REL_PATH = re.compile(r"^agents/[^/]+/(MEMORY|SOUL)\.md$")


def _roots() -> tuple[Path, ...]:
    return (repo_root().resolve(),)


@router.get("/list")
def memory_list():
    root = repo_root().resolve()
    roots = _roots()
    stale_days = get_memory_stale_days()
    cutoff = datetime.now(timezone.utc) - timedelta(days=stale_days)
    items: list[dict] = []
    for pattern in ("agents/*/MEMORY.md", "agents/*/SOUL.md"):
        for p in sorted(root.glob(pattern)):
            if not p.is_file() or not allowed_path(p, roots):
                continue
            try:
                rel = str(p.relative_to(root)).replace("\\", "/")
            except ValueError:
                continue
            if not _REL_PATH.match(rel):
                continue
            try:
                st = p.stat()
            except OSError:
                continue
            agent = rel.split("/")[1] if "/" in rel else ""
            mtime = datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
            items.append(
                {
                    "rel_path": rel,
                    "agent": agent,
                    "size_bytes": st.st_size,
                    "modified_iso": mtime.isoformat(),
                    "stale": mtime < cutoff,
                    "stale_after_days": stale_days,
                }
            )
    return envelope({"items": items})


@router.get("/file")
def memory_file(path: str = Query(..., min_length=8, max_length=512)):
    root = repo_root().resolve()
    rel = str(path).strip().replace("\\", "/").lstrip("/")
    if not _REL_PATH.match(rel):
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "Ruta no permitida para memory."}},
        )
    p = (root / rel).resolve()
    if not allowed_path(p, _roots()):
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "Fichero fuera del repo."}},
        )
    if not p.is_file():
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "Fichero no encontrado."}},
        )
    text = read_capped_text(p)
    if text is None:
        return envelope({"rel_path": rel, "error": "too_large"})
    return envelope({"rel_path": rel, "content": text})
