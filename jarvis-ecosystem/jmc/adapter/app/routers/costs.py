"""Rutas /v1/costs/*."""

from __future__ import annotations

import re

from fastapi import APIRouter, Depends, HTTPException, Query

from app.security import require_token
from app.services.cost_report import build_cost_envelope, get_cost_report_cached
from app.util_response import envelope

router = APIRouter(prefix="/costs", dependencies=[Depends(require_token)])

_MONTH_PARAM = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


def _validate_cost_month(month: str | None) -> str | None:
    if month is None or not str(month).strip():
        return None
    s = str(month).strip()
    if not _MONTH_PARAM.fullmatch(s):
        raise HTTPException(
            status_code=422,
            detail={
                "error": {
                    "code": "invalid_month",
                    "message": "Parámetro month debe ser YYYY-MM (mes 01–12).",
                }
            },
        )
    return s


@router.get("/summary")
def costs_summary(
    month: str | None = Query(None),
    include_raw: int = Query(0, ge=0, le=1, description="1 = incluir raw_tail del reporte"),
):
    month = _validate_cost_month(month)
    data = get_cost_report_cached(month=month)
    payload = build_cost_envelope(data, include_raw=bool(include_raw))
    return envelope(payload)


@router.get("/by-agent")
def costs_by_agent(
    month: str | None = Query(None),
    include_raw: int = Query(0, ge=0, le=1),
):
    month = _validate_cost_month(month)
    data = get_cost_report_cached(month=month)
    payload = build_cost_envelope(data, include_raw=bool(include_raw))
    agents = payload.get("agents") or {}
    norm = payload.get("agents_normalized") or {}
    rows = []
    for k, v in agents.items():
        row: dict = {"agent": k, "metrics": v if isinstance(v, dict) else {"raw": v}}
        if k in norm:
            row["normalized"] = norm[k]
        rows.append(row)
    return envelope(
        {
            "month": payload.get("month"),
            "agents": rows,
            "error": payload.get("error"),
        }
    )
