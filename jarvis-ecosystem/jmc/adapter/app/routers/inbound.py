"""Webhooks entrantes (sin Bearer): secreto dedicado por cabecera."""

from __future__ import annotations

import logging

from fastapi import APIRouter, Body, Header, HTTPException, Path, Request

from app.security import (
    clear_inbound_secret_failures,
    const_time_str_eq,
    record_inbound_secret_failure,
    require_inbound_secret_not_locked,
)
from app.services.telegram_inbound import (
    append_messaging_channel_event,
    inbound_expected_secret,
    inbound_secret_configured,
)
from app.util_response import envelope

router = APIRouter(prefix="/webhooks/inbound")


def _check_secret(request: Request, x_secret: str | None) -> None:
    if not inbound_secret_configured():
        raise HTTPException(
            status_code=503,
            detail={
                "error": {
                    "code": "misconfigured",
                    "message": (
                        "Define JMC_INBOUND_TELEGRAM_SECRET o JMC_INBOUND_CHANNEL_SECRET "
                        "(>=16 caracteres) para usar webhooks inbound."
                    ),
                },
            },
        )
    require_inbound_secret_not_locked(request)
    expected = inbound_expected_secret()
    got = (x_secret or "").strip()
    if not got or not const_time_str_eq(got, expected):
        record_inbound_secret_failure(request)
        raise HTTPException(
            status_code=401,
            detail={"error": {"code": "unauthorized", "message": "X-JMC-Inbound-Secret inválido o ausente"}},
        )
    clear_inbound_secret_failures(request)


def _inbound_body_handler(
    request: Request, channel: str, body: dict, x_jmc_inbound_secret: str | None
) -> dict:
    _check_secret(request, x_jmc_inbound_secret)
    if not isinstance(body, dict):
        body = {}
    direction = str(body.get("direction") or "in")
    agent = str(body.get("agent") or "jarvis")
    text = str(body.get("text") or body.get("message") or body.get("note") or "")
    if not text.strip():
        text = f"{channel} {direction}"
    pl = body.get("payload")
    extra: dict | None = pl if isinstance(pl, dict) else None
    r = append_messaging_channel_event(
        channel=channel, agent=agent, direction=direction, note=text, payload=extra
    )
    if not r.get("ok"):
        logging.getLogger(__name__).warning("inbound append_messaging_channel_event failed: %s", r)
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "log_failed",
                    "message": "No se pudo registrar el evento.",
                },
            },
        )
    return envelope(r)


@router.post("/telegram")
def inbound_telegram(
    request: Request,
    body: dict = Body(default_factory=dict),
    x_jmc_inbound_secret: str | None = Header(default=None, alias="X-JMC-Inbound-Secret"),
):
    """Ruta explícita (compatibilidad) — mismo cuerpo que `POST …/inbound/{channel}`."""
    return _inbound_body_handler(request, "telegram", body, x_jmc_inbound_secret)


@router.post("/{channel}")
def inbound_channel(
    request: Request,
    channel: str = Path(..., description="telegram | whatsapp | discord"),
    body: dict = Body(default_factory=dict),
    x_jmc_inbound_secret: str | None = Header(default=None, alias="X-JMC-Inbound-Secret"),
):
    """
    Registra un evento en activity-log (misma fuente que Activity / Overview).
    El canal fija `--task jmc-channel-<channel>` y `--kind <channel>_in|_out`.
    """
    ch = (channel or "").strip().lower()
    if ch not in ("telegram", "whatsapp", "discord"):
        raise HTTPException(
            status_code=422,
            detail={
                "error": {
                    "code": "invalid_channel",
                    "message": "Canal no soportado. Use: telegram, whatsapp o discord.",
                },
            },
        )
    return _inbound_body_handler(request, ch, body, x_jmc_inbound_secret)
