"""GET /v1/escalations."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.security import require_token
from app.services.state_store import load_escalations
from app.util_response import envelope

router = APIRouter(prefix="/escalations", dependencies=[Depends(require_token)])


@router.get("")
def list_escalations():
    return envelope({"items": load_escalations(), "doc_ref": "docs/ESCALACION_ASYNC.md"})
