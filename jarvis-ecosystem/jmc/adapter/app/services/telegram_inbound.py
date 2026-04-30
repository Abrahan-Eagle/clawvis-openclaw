"""Registrar eventos de canales de mensajería en activity-log.jsonl (vía script bash)."""

from __future__ import annotations

import json
import logging
import os
import subprocess
from pathlib import Path
from typing import Any

from app.services.paths import repo_root, state_dir

_log = logging.getLogger(__name__)
_INBOUND_CHANNELS = frozenset({"telegram", "whatsapp", "discord"})


def _activity_log_script() -> Path:
    return repo_root() / "skills" / "global" / "activity-log" / "bin" / "activity-log"


def append_activity_log_event(
    *,
    agent: str,
    task: str,
    kind: str,
    note: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Ejecuta `activity-log event` con agent/task/kind arbitrarios (JMC chat, canales, etc.)."""
    script = _activity_log_script()
    if not script.is_file():
        return {"ok": False, "error": "activity_log_script_missing", "path": str(script)}
    agent_s = (agent or "jarvis").strip()[:128]
    task_s = (task or "jmc").strip()[:256]
    kind_s = (kind or "event").strip()[:128]
    note_s = (note or "")[:2000]
    env = os.environ.copy()
    env["JARVIS_STATE_DIR"] = str(state_dir())
    root = str(repo_root())
    tmp: Path | None = None
    extra_args: list[str] = []
    if payload:
        tmp = state_dir() / "cache" / f"jmc-activity-{kind_s[:32]}-payload.json"
        tmp.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        extra_args.extend(["--payload-file", str(tmp)])
    try:
        r = subprocess.run(
            [
                "bash",
                str(script),
                "event",
                "--agent",
                agent_s,
                "--task",
                task_s,
                "--kind",
                kind_s,
                "--note",
                note_s,
                *extra_args,
            ],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    finally:
        if tmp is not None and tmp.is_file():
            try:
                tmp.unlink()
            except OSError:
                pass
    if r.returncode != 0:
        _log.warning(
            "activity-log event falló rc=%s stderr=%s",
            r.returncode,
            ((r.stderr or r.stdout or "").strip()[:500]),
        )
        return {"ok": False, "error": "activity_log_failed", "returncode": r.returncode}
    return {"ok": True, "agent": agent_s, "kind": kind_s, "task": task_s}


def append_messaging_channel_event(
    *,
    channel: str,
    agent: str,
    direction: str,
    note: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Ejecuta `activity-log event` con task `jmc-channel-<channel>` (no requiere task.json).
    channel: telegram | whatsapp | discord
    direction: in | out → <channel>_in / <channel>_out en --kind
    """
    ch = (channel or "telegram").strip().lower()
    if ch not in _INBOUND_CHANNELS:
        return {"ok": False, "error": "unknown_channel", "channel": ch, "allowed": sorted(_INBOUND_CHANNELS)}
    agent_s = (agent or "jarvis").strip()[:128]
    d = (direction or "in").strip().lower()
    kind = f"{ch}_out" if d == "out" else f"{ch}_in"
    note_s = (note or "")[:2000]
    task_id = f"jmc-channel-{ch}"
    r = append_activity_log_event(
        agent=agent_s, task=task_id, kind=kind, note=note_s, payload=payload
    )
    if not r.get("ok"):
        return r
    return {"ok": True, "agent": agent_s, "kind": kind, "channel": ch}


def append_telegram_channel_event(
    *,
    agent: str,
    direction: str,
    note: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compatibilidad: equivale a append_messaging_channel_event(channel=\"telegram\", ...)."""
    return append_messaging_channel_event(
        channel="telegram", agent=agent, direction=direction, note=note, payload=payload
    )


def inbound_secret_configured() -> bool:
    for key in ("JMC_INBOUND_CHANNEL_SECRET", "JMC_INBOUND_TELEGRAM_SECRET"):
        s = os.environ.get(key, "").strip()
        if len(s) >= 16:
            return True
    return False


def inbound_expected_secret() -> str:
    """Secreto compartido para todos los canales inbound (prioriza JMC_INBOUND_CHANNEL_SECRET)."""
    for key in ("JMC_INBOUND_CHANNEL_SECRET", "JMC_INBOUND_TELEGRAM_SECRET"):
        s = os.environ.get(key, "").strip()
        if len(s) >= 16:
            return s
    return ""
