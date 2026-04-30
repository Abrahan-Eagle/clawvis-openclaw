"""GET /v1/docs/lints."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.security import require_token
from app.services.docs_lints import run_docs_lints
from app.util_response import envelope

router = APIRouter(prefix="/docs", dependencies=[Depends(require_token)])


@router.get("/lints")
def docs_lints():
    d = run_docs_lints()
    warns = d.get("warnings") or []
    return envelope(d, warnings=warns if warns else None)
