"""Envelope JSON estándar JMC."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def envelope(data: Any, warnings: list[str] | None = None) -> dict[str, Any]:
    return {
        "data": data,
        "meta": {
            "version": "v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "warnings": warnings or [],
        },
    }
