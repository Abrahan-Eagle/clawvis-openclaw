"""GET /v1/external/healthchecks."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.security import require_token
from app.services.external_health import run_external_healthchecks
from app.util_response import envelope

router = APIRouter(prefix="/external", dependencies=[Depends(require_token)])


@router.get("/healthchecks")
def external_healthchecks():
    return envelope(run_external_healthchecks())
