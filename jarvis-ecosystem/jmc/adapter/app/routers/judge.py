"""GET /v1/judge/last."""

from __future__ import annotations

import json

from fastapi import APIRouter, Depends

from app.security import allowed_path, require_token, sanitize_obj
from app.services.read_capped import read_capped_text
from app.services.paths import judge_dir, repo_root
from app.util_response import envelope

router = APIRouter(prefix="/judge", dependencies=[Depends(require_token)])


@router.get("/last")
def judge_last():
    roots = (repo_root(), judge_dir())
    jd = judge_dir()
    if not jd.is_dir():
        return envelope({"runs": [], "note": "state/judge/ vacío o ausente"})

    files = sorted(jd.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:20]
    runs = []
    for p in files:
        if not allowed_path(p, roots):
            continue
        text = read_capped_text(p)
        if text is None:
            continue
        try:
            raw = json.loads(text)
        except json.JSONDecodeError:
            continue
        runs.append({"file": p.name, "mtime": p.stat().st_mtime, "summary": sanitize_obj(raw)})

    return envelope({"runs": runs})
