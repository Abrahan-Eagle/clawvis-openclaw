"""Rutas públicas (sin Bearer): estado de lockout y reporte CSP."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, Request

from app.security import auth_status_for_request
from app.services.csp_report_store import push_csp_report
from app.util_response import envelope

router = APIRouter()


@router.get("/auth/status")
def auth_status(request: Request):
    return envelope(auth_status_for_request(request))


@router.post("/csp-report")
async def csp_report(body: Any = Body(None)):
    """Acepta cuerpo JSON del navegador; almacena en memoria (cap 500)."""
    push_csp_report(body if body is not None else {})
    return envelope({"ok": True})
