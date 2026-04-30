"""Rutas dentro del repo y openclaw home."""

from __future__ import annotations

import os
from pathlib import Path

from app.config import get_repo_root
from app.security import allowed_path


def repo_root() -> Path:
    return get_repo_root()


def openclaw_json_path() -> Path:
    raw = os.environ.get("JMC_OPENCLAW_JSON_PATH", "").strip()
    if raw:
        return Path(raw).expanduser().resolve()
    home = Path.home() / ".openclaw" / "openclaw.json"
    if home.is_file():
        return home
    snap = repo_root() / "openclaw.json"
    if snap.is_file():
        return snap
    legacy = repo_root() / "config" / "openclaw-home" / "openclaw.json"
    if legacy.is_file():
        return legacy
    return snap  # preferencia doc si no existe


def state_dir() -> Path:
    return Path(os.environ.get("JMC_STATE_DIR", str(repo_root() / "state")))


def client_dossiers_dir() -> Path:
    return repo_root() / "client-dossiers"


def automations_dir() -> Path:
    return repo_root() / "automations"


def docs_dir() -> Path:
    return repo_root() / "docs"


def scripts_dir() -> Path:
    return repo_root() / "scripts"


def cost_report_script() -> Path:
    return scripts_dir() / "cost-report.sh"


def sync_automations_script() -> Path:
    return scripts_dir() / "sync-automations-yaml.sh"


def judge_dir() -> Path:
    return state_dir() / "judge"


def activity_log_path() -> Path:
    return state_dir() / "activity-log.jsonl"


def tasks_dir() -> Path:
    return state_dir() / "tasks"


def handoffs_dir() -> Path:
    return state_dir() / "handoffs"


def chat_inbox_dir() -> Path:
    """Directorio del buzón JMC Chat (`state/jmc-inbox` por defecto).

    Si `JMC_CHAT_INBOX_DIR` es absoluto, debe quedar bajo `repo_root()` o `state_dir()`
    salvo `JMC_CHAT_INBOX_ALLOW_EXTERNAL=1` (riesgo operativo explícito).
    """
    raw = os.environ.get("JMC_CHAT_INBOX_DIR", "").strip()
    if raw:
        p = Path(raw).expanduser().resolve()
        allow_ext = os.environ.get("JMC_CHAT_INBOX_ALLOW_EXTERNAL", "").strip().lower() in (
            "1",
            "true",
            "yes",
        )
        if not allow_ext:
            roots = (repo_root().resolve(), state_dir().resolve())
            if not allowed_path(p, roots):
                raise ValueError(
                    "JMC_CHAT_INBOX_DIR debe estar bajo el repo o state/ "
                    "(o define JMC_CHAT_INBOX_ALLOW_EXTERNAL=1 si aceptas otra ruta)."
                )
        return p
    return state_dir() / "jmc-inbox"


def allowed_search_roots() -> tuple[Path, ...]:
    r = repo_root()
    oc = openclaw_json_path().parent
    roots = [r, oc]
    sd = state_dir()
    if sd.exists():
        roots.append(sd)
    return tuple(dict.fromkeys(roots))
