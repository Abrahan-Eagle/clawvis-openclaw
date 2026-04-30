"""Healthchecks HTTP externos con whitelist."""

from __future__ import annotations

import ipaddress
import logging
import os
import socket
import urllib.error
import urllib.request
from typing import Any
from urllib.parse import urlparse


def _parse_entries() -> list[tuple[str, str]]:
    raw = os.environ.get("JMC_EXT_HEALTHCHECKS", "").strip()
    if not raw:
        return []
    out: list[tuple[str, str]] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if "|" in part:
            name, url = part.split("|", 1)
            out.append((name.strip()[:64], url.strip()[:512]))
        else:
            out.append(("check", part[:512]))
    return out[:8]


def _host_allowed(host: str, allow_local: bool) -> bool:
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


def run_external_healthchecks() -> dict[str, Any]:
    allow_local = os.environ.get("JMC_EXT_ALLOW_LOCAL", "").strip() in ("1", "true", "yes")
    results: list[dict[str, Any]] = []
    for name, url in _parse_entries():
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            results.append({"name": name, "url": url, "ok": False, "error": "invalid_scheme"})
            continue
        host = parsed.hostname or ""
        if not host or not _host_allowed(host, allow_local):
            results.append({"name": name, "url": url, "ok": False, "error": "host_not_allowed"})
            continue
        try:
            req = urllib.request.Request(url, method="GET", headers={"User-Agent": "jmc-adapter/1.10"})
            with urllib.request.urlopen(req, timeout=3) as r:
                ok = 200 <= r.getcode() < 400
                results.append({"name": name, "url": url, "ok": ok, "status": r.getcode()})
        except urllib.error.HTTPError as e:
            results.append({"name": name, "url": url, "ok": False, "status": e.code, "error": "http_error"})
        except Exception as e:
            _log.warning("external healthcheck %s %s: %s", name, url, e)
            results.append({"name": name, "url": url, "ok": False, "error": "request_failed"})
    return {"items": results}
