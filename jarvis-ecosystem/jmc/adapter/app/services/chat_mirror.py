"""Espejo opcional: `openclaw message send` (Telegram / Discord)."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

_ALLOWED = frozenset({"telegram", "discord"})


def mirror_channels_allowed() -> list[str]:
    raw = (os.environ.get("JMC_CHAT_MIRROR_CHANNELS") or "telegram,discord").strip()
    parts = [p.strip().lower() for p in raw.split(",") if p.strip()]
    return [p for p in parts if p in _ALLOWED] or ["telegram", "discord"]


def mirror_enabled() -> bool:
    return os.environ.get("JMC_CHAT_MIRROR_ENABLED", "").strip().lower() in ("1", "true", "yes")


def openclaw_bin_path() -> Path:
    raw = (os.environ.get("JMC_OPENCLAW_BIN") or "openclaw").strip()
    p = Path(raw).expanduser()
    if p.is_file():
        return p.resolve()
    w = shutil.which(raw)
    if w:
        return Path(w).resolve()
    return p


def mirror_to_channel(*, channel: str, text: str) -> dict[str, Any]:
    """
    Envía texto por `openclaw message send --channel <ch> --text ...`.
    No adjunta binarios (solo resumen en texto); el buzón en disco sigue siendo la fuente de verdad.
    """
    ch = (channel or "").strip().lower()
    if ch not in _ALLOWED:
        return {"ok": False, "error": "invalid_mirror_channel", "channel": ch}
    note = (text or "")[:8000]
    if not note.strip():
        return {"ok": False, "error": "empty_text"}
    bin_path = openclaw_bin_path()
    if not bin_path.is_file():
        return {"ok": False, "warning": "openclaw_bin_missing", "path": str(bin_path)}
    try:
        r = subprocess.run(
            [str(bin_path), "message", "send", "--channel", ch, "--text", note],
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return {"ok": False, "error": "mirror_exec_failed"}
    if r.returncode != 0:
        return {"ok": False, "error": "mirror_command_failed", "returncode": r.returncode}
    return {"ok": True, "channel": ch}
