"""GET /v1/files/* — árbol y lectura acotada (docs / skills / automations / agents)."""

from __future__ import annotations

import re
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query

from app.security import allowed_path, require_token
from app.services.paths import automations_dir, docs_dir, repo_root
from app.services.read_capped import read_capped_text
from app.util_response import envelope

router = APIRouter(prefix="/files", dependencies=[Depends(require_token)])

_ALLOWED_EXT = frozenset({".md", ".yaml", ".yml", ".json", ".txt"})
_PATH_SAFE = re.compile(r"^[A-Za-z0-9._/\-]+$")


def _root_path(name: str) -> Path:
    r = repo_root().resolve()
    if name == "docs":
        return docs_dir().resolve()
    if name == "skills":
        return (r / "skills").resolve()
    if name == "automations":
        return automations_dir().resolve()
    if name == "agents":
        return (r / "agents").resolve()
    raise KeyError(name)


def _resolve_under(root: Path, sub: str) -> Path:
    sub = (sub or "").strip().replace("\\", "/").lstrip("/")
    if sub and not _PATH_SAFE.fullmatch(sub):
        raise HTTPException(
            status_code=400,
            detail={"error": {"code": "invalid_path", "message": "Caracteres no permitidos en path."}},
        )
    p = (root / sub).resolve() if sub else root.resolve()
    if not allowed_path(p, (root,)):
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "Ruta fuera del árbol permitido."}},
        )
    return p


@router.get("/tree")
def files_tree(
    root: str = Query(..., min_length=3, max_length=32),
    max_entries: int = Query(400, ge=10, le=2000),
):
    if root not in ("docs", "skills", "automations", "agents"):
        raise HTTPException(
            status_code=422,
            detail={
                "error": {
                    "code": "invalid_root",
                    "message": "root debe ser docs, skills, automations o agents.",
                },
            },
        )
    base = _root_path(root)
    rrepo = repo_root().resolve()
    if not base.is_dir():
        return envelope({"root": root, "entries": []})
    entries: list[dict] = []
    count = 0
    for p in sorted(base.rglob("*")):
        if count >= max_entries:
            break
        if not allowed_path(p, (base, rrepo)):
            continue
        try:
            rel = str(p.relative_to(base)).replace("\\", "/")
        except ValueError:
            continue
        if p.is_dir():
            entries.append({"path": rel or ".", "type": "dir", "size": None})
            count += 1
        elif p.is_file():
            suf = p.suffix.lower()
            if suf not in _ALLOWED_EXT and suf != "":
                continue
            try:
                sz = p.stat().st_size
            except OSError:
                continue
            entries.append({"path": rel, "type": "file", "size": sz})
            count += 1
    return envelope({"root": root, "entries": entries, "truncated": count >= max_entries})


@router.get("/get")
def files_get(
    root: str = Query(..., min_length=3, max_length=32),
    path: str = Query(..., min_length=1, max_length=512),
):
    if root not in ("docs", "skills", "automations", "agents"):
        raise HTTPException(
            status_code=422,
            detail={
                "error": {
                    "code": "invalid_root",
                    "message": "root debe ser docs, skills, automations o agents.",
                },
            },
        )
    base = _root_path(root)
    p = _resolve_under(base, path)
    if not p.is_file():
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "No es un fichero."}},
        )
    suf = p.suffix.lower()
    if suf not in _ALLOWED_EXT:
        raise HTTPException(
            status_code=400,
            detail={"error": {"code": "invalid_extension", "message": "Extensión no permitida."}},
        )
    text = read_capped_text(p)
    if text is None:
        return envelope({"root": root, "path": path, "error": "too_large"})
    return envelope({"root": root, "path": path, "content": text})
