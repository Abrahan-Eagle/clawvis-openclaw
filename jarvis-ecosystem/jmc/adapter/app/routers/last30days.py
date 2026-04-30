"""GET /v1/last30days — agregados desde activity-log.jsonl."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.security import require_token
from app.services.jsonl_reader import aggregate_last30days
from app.services.paths import activity_log_path
from app.util_response import envelope

router = APIRouter(prefix="/last30days", dependencies=[Depends(require_token)])


@router.get("")
def last30days():
    data = aggregate_last30days(activity_log_path())
    return envelope(data)
