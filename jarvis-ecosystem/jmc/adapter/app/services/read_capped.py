"""Lecturas acotadas por tamaño de fichero (defensa DoS / RAM)."""

from __future__ import annotations

from pathlib import Path

DEFAULT_MAX_READ_BYTES = 512_000


def read_capped_text(path: Path, *, max_bytes: int = DEFAULT_MAX_READ_BYTES) -> str | None:
    """Lee texto UTF-8 si el tamaño en disco es <= max_bytes; si no, devuelve None."""
    try:
        sz = path.stat().st_size
    except OSError:
        return None
    if sz > max_bytes:
        return None
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
