"""Bearer auth y helpers."""

from __future__ import annotations

import hashlib
import hmac
import os
import re
import threading
import time
from collections import deque
from pathlib import Path

from fastapi import Depends, HTTPException, Request, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import get_auth_fail_max, get_auth_fail_window_sec, get_bearer_token

_bearer = HTTPBearer(auto_error=False)

_AUTH_LOCK = threading.Lock()
# IP -> deque de time.monotonic() en fallos recientes
_auth_failures: dict[str, deque[float]] = {}
# IP -> monotonic hasta el que la IP queda bloqueada
_auth_locked_until: dict[str, float] = {}

# Lockout separado para X-JMC-Inbound-Secret (clave "inbound:<ip>")
_inbound_failures: dict[str, deque[float]] = {}
_inbound_locked_until: dict[str, float] = {}

def const_time_str_eq(a: str, b: str) -> bool:
    """Compara dos strings (p. ej. secretos) vía digest SHA-256 + compare_digest (longitud fija)."""
    try:
        da = hashlib.sha256(a.encode("utf-8")).digest()
        db = hashlib.sha256(b.encode("utf-8")).digest()
        return hmac.compare_digest(da, db)
    except Exception:
        return False


_SECRET_KEY_RE = re.compile(
    r"(token|secret|password|api_key|apikey|consumerkey|authorization|bearer)",
    re.I,
)


def _client_ip(request: Request) -> str:
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


def _is_auth_locked(ip: str) -> bool:
    until = _auth_locked_until.get(ip)
    if until is None:
        return False
    now = time.monotonic()
    if now >= until:
        with _AUTH_LOCK:
            _auth_locked_until.pop(ip, None)
            _auth_failures.pop(ip, None)
        return False
    return True


def _record_auth_failure(ip: str) -> None:
    window = float(get_auth_fail_window_sec())
    max_f = get_auth_fail_max()
    now = time.monotonic()
    with _AUTH_LOCK:
        dq = _auth_failures.setdefault(ip, deque())
        dq.append(now)
        while dq and dq[0] < now - window:
            dq.popleft()
        if len(dq) >= max_f:
            _auth_locked_until[ip] = now + window


def _clear_auth_failures(ip: str) -> None:
    with _AUTH_LOCK:
        _auth_failures.pop(ip, None)
        _auth_locked_until.pop(ip, None)


def _inbound_ip_key(request: Request) -> str:
    return "inbound:" + _client_ip(request)


def _is_inbound_locked(ipk: str) -> bool:
    until = _inbound_locked_until.get(ipk)
    if until is None:
        return False
    now = time.monotonic()
    if now >= until:
        with _AUTH_LOCK:
            _inbound_locked_until.pop(ipk, None)
            _inbound_failures.pop(ipk, None)
        return False
    return True


def require_inbound_secret_not_locked(request: Request) -> None:
    ipk = _inbound_ip_key(request)
    if _is_inbound_locked(ipk):
        raise HTTPException(
            status_code=429,
            detail={
                "error": {
                    "code": "inbound_locked",
                    "message": "Demasiados intentos fallidos en inbound; reintenta más tarde.",
                }
            },
        )


def record_inbound_secret_failure(request: Request) -> None:
    window = float(get_auth_fail_window_sec())
    max_f = get_auth_fail_max()
    now = time.monotonic()
    ipk = _inbound_ip_key(request)
    with _AUTH_LOCK:
        dq = _inbound_failures.setdefault(ipk, deque())
        dq.append(now)
        while dq and dq[0] < now - window:
            dq.popleft()
        if len(dq) >= max_f:
            _inbound_locked_until[ipk] = now + window


def clear_inbound_secret_failures(request: Request) -> None:
    ipk = _inbound_ip_key(request)
    with _AUTH_LOCK:
        _inbound_failures.pop(ipk, None)
        _inbound_locked_until.pop(ipk, None)


def auth_status_for_request(request: Request) -> dict[str, object]:
    """Estado de lockout por IP (sin Bearer). Usado por GET /v1/auth/status."""
    ip = _client_ip(request)
    ipk = _inbound_ip_key(request)
    now = time.monotonic()
    with _AUTH_LOCK:
        until = _auth_locked_until.get(ip)
        locked = until is not None and now < until
        retry = 0.0
        if locked and until is not None:
            retry = max(0.0, until - now)
        dq = _auth_failures.get(ip)
        nfail = len(dq) if dq else 0
        in_until = _inbound_locked_until.get(ipk)
        inbound_locked = in_until is not None and now < in_until
        inbound_retry = 0.0
        if inbound_locked and in_until is not None:
            inbound_retry = max(0.0, in_until - now)
        idq = _inbound_failures.get(ipk)
        inbound_fails = len(idq) if idq else 0
    return {
        "locked": locked,
        "fails": nfail,
        "retry_after_sec": int(retry) + (1 if retry > 0 else 0),
        "inbound_locked": inbound_locked,
        "inbound_fails": inbound_fails,
        "inbound_retry_after_sec": int(inbound_retry) + (1 if inbound_retry > 0 else 0),
    }


def require_token(
    request: Request,
    creds: HTTPAuthorizationCredentials | None = Security(_bearer),
) -> None:
    ip = _client_ip(request)
    if _is_auth_locked(ip):
        raise HTTPException(
            status_code=429,
            detail={
                "error": {
                    "code": "auth_locked",
                    "message": "Demasiados intentos fallidos; reintenta más tarde.",
                }
            },
        )
    expected = get_bearer_token()
    if len(expected) < 32:
        raise HTTPException(
            status_code=503,
            detail={
                "error": {
                    "code": "misconfigured",
                    "message": "JMC_BEARER_TOKEN debe tener >= 32 caracteres",
                }
            },
        )
    if creds is None or not const_time_str_eq(creds.credentials or "", expected):
        _record_auth_failure(ip)
        raise HTTPException(
            status_code=401,
            detail={"error": {"code": "unauthorized", "message": "Bearer inválido o ausente"}},
        )
    _clear_auth_failures(ip)


def sanitize_obj(obj):
    """Elimina o redacta claves sensibles en dict/list anidados."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            ks = str(k)
            if _SECRET_KEY_RE.search(ks):
                out[ks] = "[redacted]"
                continue
            out[ks] = sanitize_obj(v)
        return out
    if isinstance(obj, list):
        return [sanitize_obj(x) for x in obj]
    return obj


def allowed_path(path: Path, roots: tuple[Path, ...]) -> bool:
    try:
        rp = path.resolve()
    except OSError:
        return False
    for root in roots:
        try:
            r = root.resolve()
        except OSError:
            continue
        try:
            rp.relative_to(r)
            return True
        except ValueError:
            continue
    return False
