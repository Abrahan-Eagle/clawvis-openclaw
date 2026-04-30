"""GET /v1/search — búsqueda read-only en markdown/yaml bajo el repo."""

from __future__ import annotations

import threading
import time
from pathlib import Path

from fastapi import APIRouter, Depends, Query

from app.security import allowed_path, require_token
from app.services.paths import repo_root
from app.services.read_capped import read_capped_text
from app.util_response import envelope

router = APIRouter(prefix="/search", dependencies=[Depends(require_token)])

_CACHE_LOCK = threading.Lock()
_CACHE: dict[str, tuple[float, list[dict]]] = {}
_TTL = 30.0

_GLOBS = (
    "docs/**/*.md",
    "agents/**/MEMORY.md",
    "skills/**/SKILL.md",
    "automations/**/*.yaml",
    "automations/**/*.yml",
)


def _collect_paths(root: Path, max_files: int = 600) -> list[Path]:
    out: list[Path] = []
    seen: set[Path] = set()
    rr = root.resolve()
    for pattern in _GLOBS:
        for p in root.glob(pattern):
            if len(out) >= max_files:
                return out
            if not p.is_file():
                continue
            try:
                rp = p.resolve()
            except OSError:
                continue
            if rp in seen:
                continue
            if not allowed_path(rp, (rr,)):
                continue
            seen.add(rp)
            out.append(rp)
    return out


def _run_search(q: str, limit: int) -> list[dict]:
    q_lower = q.strip().lower()
    if len(q_lower) < 2:
        return []
    root = repo_root().resolve()
    hits: list[dict] = []
    for p in _collect_paths(root):
        text = read_capped_text(p)
        if not text:
            continue
        try:
            rel = str(p.relative_to(root)).replace("\\", "/")
        except ValueError:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            if q_lower in line.lower():
                snip = line.strip()
                if len(snip) > 240:
                    snip = snip[:237] + "…"
                hits.append({"rel_path": rel, "line": i, "snippet": snip, "score": 1})
                if len(hits) >= limit:
                    return hits
    return hits


@router.get("/")
def search_get(
    q: str = Query("", min_length=0, max_length=200),
    limit: int = Query(50, ge=1, le=200),
):
    key = f"{q}\0{limit}"
    now = time.monotonic()
    with _CACHE_LOCK:
        hit = _CACHE.get(key)
        if hit and now - hit[0] < _TTL:
            return envelope({"query": q, "hits": hit[1]})
    data = _run_search(q, limit)
    with _CACHE_LOCK:
        _CACHE[key] = (now, data)
        if len(_CACHE) > 64:
            oldest = min(_CACHE.items(), key=lambda kv: kv[1][0])
            _CACHE.pop(oldest[0], None)
    return envelope({"query": q, "hits": data})
