"""GET /v1/runtime/services — estado systemd/PM2 (lista blanca)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.security import require_token
from app.services.runtime_services import load_runtime_services
from app.util_response import envelope

router = APIRouter(prefix="/runtime", dependencies=[Depends(require_token)])


@router.get("/services")
def runtime_services(journal_lines: int = Query(0, ge=0, le=20)):
    return envelope(load_runtime_services(journal_lines=journal_lines))
