"""GET /v1/diagnostics."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.security import require_token
from app.services.diagnostics_info import build_diagnostics
from app.util_response import envelope

router = APIRouter(prefix="/diagnostics", dependencies=[Depends(require_token)])


@router.get("")
def diagnostics():
    return envelope(build_diagnostics())
