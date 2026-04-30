"""GET /v1/gates."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.security import require_token
from app.services.gates_parser import parse_approval_gates
from app.util_response import envelope

router = APIRouter(prefix="/gates", dependencies=[Depends(require_token)])


@router.get("")
def list_gates():
    gates = parse_approval_gates()
    warnings = []
    if not gates:
        warnings.append("No se pudieron parsear gates (¿APPROVAL_GATES.md cambió?)")
    return envelope({"gates": gates, "doc_ref": "docs/APPROVAL_GATES.md"}, warnings=warnings)
