"""Validación y guardado de adjuntos del chat JMC."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import BinaryIO

_BLOCKED_EXT = frozenset(
    {
        ".sh",
        ".bat",
        ".cmd",
        ".exe",
        ".dll",
        ".so",
        ".ps1",
        ".msi",
        ".scr",
        ".com",
    }
)
_CHUNK = 1024 * 1024


def max_file_bytes() -> int:
    raw = (os.environ.get("JMC_CHAT_MAX_FILE_BYTES") or "26214400").strip()
    try:
        v = int(raw, 10)
    except ValueError:
        v = 26214400
    return max(1024, min(v, 104857600))


def max_files_per_message() -> int:
    raw = (os.environ.get("JMC_CHAT_MAX_FILES_PER_MSG") or "5").strip()
    try:
        v = int(raw, 10)
    except ValueError:
        v = 5
    return max(1, min(v, 10))


def sanitize_basename(original: str) -> str:
    """Nombre seguro para disco; exige extensión y bloquea ejecutables."""
    base = Path(str(original or "")).name.strip()
    if not base or base in (".", ".."):
        raise ValueError("invalid_filename")
    if "." not in base:
        raise ValueError("extension_required")
    ext = base[base.rfind(".") :].lower()
    if ext in _BLOCKED_EXT:
        raise ValueError("blocked_extension")
    stem, dot, suf = base.rpartition(".")
    if not stem:
        raise ValueError("invalid_filename")
    stem_clean = re.sub(r"[^a-zA-Z0-9._-]+", "_", stem).strip("._") or "file"
    suf_clean = re.sub(r"[^a-zA-Z0-9]+", "", suf)[:16].lower() or "bin"
    out = f"{stem_clean[:180]}.{suf_clean}"
    if "." not in out:
        raise ValueError("invalid_filename")
    ext2 = out[out.rfind(".") :].lower()
    if ext2 in _BLOCKED_EXT:
        raise ValueError("blocked_extension")
    return out


def save_stream_capped(stream: BinaryIO, dest: Path, *, max_bytes: int) -> int:
    """Escribe stream a dest truncando lectura a max_bytes; devuelve bytes escritos."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with dest.open("wb") as out:
        while True:
            chunk = stream.read(_CHUNK)
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                raise ValueError("file_too_large")
            out.write(chunk)
    return total
