"""POST /v1/webhooks/test — prueba de webhook firmado."""

from __future__ import annotations

from fastapi import APIRouter, Body, Depends

from app.security import require_token
from app.services.webhook_send import send_webhook_payload, webhook_configured
from app.util_response import envelope

router = APIRouter(prefix="/webhooks", dependencies=[Depends(require_token)])


@router.get("/status")
def webhook_status():
    return envelope({"configured": webhook_configured()})


@router.post("/test")
def webhook_test():
    r = send_webhook_payload({"event": "jmc.test", "message": "smoke webhook"})
    return envelope(r)


@router.post("/notify")
def webhook_notify(payload: dict = Body(...)):
    """Dispara un POST al webhook configurado con el JSON del cliente (acotado)."""
    body = dict(payload) if isinstance(payload, dict) else {"body": str(payload)[:2000]}
    if len(str(body)) > 8000:
        return envelope({"sent": False, "error": "payload too large"}, warnings=["max ~8KB"])
    r = send_webhook_payload({"event": "jmc.notify", "payload": body})
    return envelope(r)
