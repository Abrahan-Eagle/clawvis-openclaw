"""GET /v1/dossiers."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, Depends

from app.security import allowed_path, sanitize_obj, require_token
from app.services.paths import client_dossiers_dir, repo_root
from app.services.read_capped import read_capped_text
from app.util_response import envelope

router = APIRouter(prefix="/dossiers", dependencies=[Depends(require_token)])


def _append_cli_json(p: Path, roots: tuple[Path, ...], items: list[dict]) -> None:
    if not allowed_path(p, roots):
        return
    text = read_capped_text(p)
    if text is None:
        items.append({"id": p.stem, "file": p.name, "error": "too_large"})
        return
    try:
        raw = json.loads(text)
    except json.JSONDecodeError:
        return
    items.append({"id": p.stem, "file": p.name, "data": sanitize_obj(raw)})


def _append_cli_folder(sub: Path, roots: tuple[Path, ...], items: list[dict]) -> None:
    """Carpeta cli-* (p. ej. cli-DEMO-rrss/) con brand.json u otro JSON legible."""
    if not sub.is_dir() or not allowed_path(sub, roots):
        return
    name = sub.name
    if not name.startswith("cli-"):
        return
    brand = sub / "brand.json"
    candidates = [brand] if brand.is_file() else sorted(sub.glob("*.json"))
    for cand in candidates:
        if not cand.is_file() or not allowed_path(cand, roots):
            continue
        text = read_capped_text(cand)
        if text is None:
            items.append({"id": name, "file": f"{name}/", "source_file": cand.name, "error": "too_large"})
            return
        try:
            raw = json.loads(text)
        except json.JSONDecodeError:
            continue
        items.append(
            {
                "id": name,
                "file": f"{name}/",
                "source_file": cand.name,
                "data": sanitize_obj(raw),
            }
        )
        return
    items.append(
        {
            "id": name,
            "file": f"{name}/",
            "source_file": None,
            "data": {},
            "note": "folder_without_readable_json",
        }
    )


@router.get("")
def list_dossiers():
    roots = (repo_root(), client_dossiers_dir())
    d = client_dossiers_dir()
    items: list[dict] = []
    if not d.is_dir():
        return envelope({"items": []})

    for p in sorted(d.glob("cli-*.json")):
        _append_cli_json(p, roots, items)

    seen_ids = {str(i.get("id") or "") for i in items if i.get("id")}
    for sub in sorted(d.iterdir()):
        if not sub.is_dir() or not sub.name.startswith("cli-"):
            continue
        if sub.name in seen_ids:
            continue
        _append_cli_folder(sub, roots, items)

    items.sort(key=lambda x: str(x.get("id") or ""))
    return envelope({"items": items})
