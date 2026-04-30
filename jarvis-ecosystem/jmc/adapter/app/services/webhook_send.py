"""Webhook outbound opcional (HMAC-SHA256)."""

from __future__ import annotations

import hashlib
import hmac
import ipaddress
import json
import logging
import os
import socket
import urllib.error
import urllib.request
from typing import Any
from urllib.parse import urlparse

_log = logging.getLogger(__name__)


def webhook_configured() -> bool:
    return bool(os.environ.get("JMC_WEBHOOK_URL", "").strip())


def _webhook_url_allowed(url: str) -> bool:
    try:
        p = urlparse(url)
        return p.scheme in ("http", "https") and bool(p.netloc)
    except Exception:
        return False


def _webhook_host_allowed(host: str) -> bool:
    """Rechaza IPs privadas / loopback salvo JMC_WEBHOOK_ALLOW_LOCAL (mismo criterio que healthchecks externos)."""
    allow_local = os.environ.get("JMC_WEBHOOK_ALLOW_LOCAL", "").strip().lower() in ("1", "true", "yes")
    try:
        infos = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
    except OSError:
        return False
    for info in infos:
        ip = info[4][0]
        try:
            addr = ipaddress.ip_address(ip)
        except ValueError:
            continue
        if addr.is_loopback:
            return bool(allow_local)
        if addr.is_private or addr.is_link_local or addr.is_reserved:
            return False
    return True


def send_webhook_payload(payload: dict[str, Any], timeout: float = 5.0) -> dict[str, Any]:
    url = os.environ.get("JMC_WEBHOOK_URL", "").strip()
    secret = os.environ.get("JMC_WEBHOOK_SECRET", "").strip()
    if not url:
        return {"sent": False, "error": "JMC_WEBHOOK_URL no configurado"}
    if not _webhook_url_allowed(url):
        return {"sent": False, "error": "JMC_WEBHOOK_URL inválido (solo http/https con host)"}
    parsed = urlparse(url)
    whost = parsed.hostname or ""
    if not whost or not _webhook_host_allowed(whost):
        return {"sent": False, "error": "webhook_host_not_allowed"}
    body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json", "User-Agent": "jmc-adapter/1.10"}
    if secret:
        sig = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
        headers["X-JMC-Signature"] = sig
    try:
        req = urllib.request.Request(url, data=body, method="POST", headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return {"sent": True, "status": r.getcode()}
    except urllib.error.HTTPError as e:
        return {"sent": False, "status": e.code, "error": "webhook_http_error"}
    except Exception as e:
        _log.warning("webhook send failed: %s", e)
        return {"sent": False, "error": "webhook_send_failed"}
