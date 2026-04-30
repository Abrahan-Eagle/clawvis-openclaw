"""GET /v1/heartbeats/coverage."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.security import require_token
from app.services.heartbeats_coverage import build_heartbeats_coverage
from app.util_response import envelope

router = APIRouter(prefix="/heartbeats", dependencies=[Depends(require_token)])


@router.get("/coverage")
def heartbeats_coverage():
    return envelope(build_heartbeats_coverage())
