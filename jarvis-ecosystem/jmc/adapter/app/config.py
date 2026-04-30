"""Configuración desde env y rutas repo."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path


def _infer_repo_root() -> Path:
    here = Path(__file__).resolve()
    # jarvis-ecosystem/jmc/adapter/app/config.py -> parents[3] = jarvis-ecosystem
    return here.parents[3]


@lru_cache
def get_repo_root() -> Path:
    raw = os.environ.get("JMC_REPO_ROOT", "").strip()
    if raw:
        return Path(raw).resolve()
    return _infer_repo_root()


def get_bind() -> str:
    return os.environ.get("JMC_BIND", "127.0.0.1").strip() or "127.0.0.1"


def get_port() -> int:
    raw = os.environ.get("JMC_PORT", "8765").strip()
    try:
        port = int(raw, 10)
    except ValueError as e:
        raise ValueError(f"JMC_PORT inválido ({raw!r}): debe ser un entero 1–65535") from e
    if port < 1 or port > 65535:
        raise ValueError(f"JMC_PORT fuera de rango: {port} (use 1–65535)")
    return port


def get_bearer_token() -> str:
    return os.environ.get("JMC_BEARER_TOKEN", "").strip()


def get_cors_origin() -> str | None:
    v = os.environ.get("JMC_CORS_ORIGIN", "").strip()
    return v or None


def get_cors_origins() -> list[str]:
    """Uno o varios orígenes (CSV). Vacío = sin CORS middleware."""
    raw = os.environ.get("JMC_CORS_ORIGIN", "").strip()
    if not raw:
        return []
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    return parts[:16]


BUILD_TIME = os.environ.get("JMC_BUILD_TIME", "dev")


def get_brand() -> dict[str, str]:
    """Branding opcional (v1.9+) desde env; sin secretos."""
    tw = (os.environ.get("JMC_BRAND_TWITTER", "") or "").strip()[:64]
    return {
        "name": os.environ.get("JMC_BRAND_NAME", "Jarvis Mission Control").strip() or "Jarvis Mission Control",
        "emoji": (os.environ.get("JMC_BRAND_EMOJI", "") or "").strip()[:8],
        "avatar": (os.environ.get("JMC_BRAND_AVATAR", "") or "").strip()[:512],
        "company": (os.environ.get("JMC_BRAND_COMPANY", "") or "").strip()[:120],
        "owner": (os.environ.get("JMC_BRAND_OWNER", "") or "").strip()[:120],
        "description": (os.environ.get("JMC_BRAND_DESCRIPTION", "") or "").strip()[:400],
        "location": (os.environ.get("JMC_BRAND_LOCATION", "") or "").strip()[:120],
        "birth_date": (os.environ.get("JMC_BRAND_BIRTH_DATE", "") or "").strip()[:32],
        "social": tw,
    }


def get_auth_fail_max() -> int:
    raw = os.environ.get("JMC_AUTH_FAIL_MAX", "10").strip()
    try:
        n = int(raw, 10)
    except ValueError:
        return 10
    return max(3, min(n, 100))


def get_auth_fail_window_sec() -> int:
    raw = os.environ.get("JMC_AUTH_FAIL_WINDOW", "900").strip()
    try:
        n = int(raw, 10)
    except ValueError:
        return 900
    return max(60, min(n, 86_400))


def get_task_zombie_hours() -> float:
    raw = os.environ.get("JMC_TASK_ZOMBIE_HOURS", "72").strip()
    try:
        h = float(raw)
    except ValueError:
        return 72.0
    return max(1.0, min(h, 720.0))


def get_memory_stale_days() -> int:
    raw = os.environ.get("JMC_MEMORY_STALE_DAYS", "14").strip()
    try:
        d = int(raw, 10)
    except ValueError:
        return 14
    return max(1, min(d, 365))
