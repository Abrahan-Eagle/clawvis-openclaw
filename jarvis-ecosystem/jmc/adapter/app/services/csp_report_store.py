"""Almacén circular en memoria para reportes CSP (POST /v1/csp-report)."""

from __future__ import annotations

import threading
import time
from collections import deque
from typing import Any

_MAX = 500
_LOCK = threading.Lock()
_reports: deque[dict[str, Any]] = deque(maxlen=_MAX)


def push_csp_report(body: dict[str, Any] | list[Any] | str | None) -> None:
    entry = {"ts": time.time(), "body": body if isinstance(body, (dict, list, str)) else str(body)[:2000]}
    with _LOCK:
        _reports.append(entry)


def list_csp_reports(limit: int = 20) -> list[dict[str, Any]]:
    lim = max(1, min(limit, 100))
    with _LOCK:
        return list(_reports)[-lim:]


def reset_csp_reports_for_tests() -> None:
    """Solo tests: vacía la cola CSP."""
    with _LOCK:
        _reports.clear()
