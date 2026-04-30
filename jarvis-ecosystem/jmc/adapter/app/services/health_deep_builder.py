"""Agregado read-only para GET /v1/health/deep."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

from app.config import get_repo_root
from app.services.automations_diff import run_sync_check
from app.services.paths import (
    activity_log_path,
    automations_dir,
    client_dossiers_dir,
    judge_dir,
    openclaw_json_path,
    state_dir,
    tasks_dir,
)
from app.services.read_capped import read_capped_text


def _dir_bytes(p: Path, cap_files: int = 5000) -> tuple[int, int]:
    if not p.is_dir():
        return 0, 0
    total = 0
    n = 0
    try:
        for child in p.rglob("*"):
            if n >= cap_files:
                break
            if child.is_file():
                try:
                    total += child.stat().st_size
                    n += 1
                except OSError:
                    continue
    except OSError:
        return 0, 0
    return total, n


def _file_meta(p: Path) -> dict[str, Any]:
    if not p.is_file():
        return {"exists": False, "size_bytes": 0, "modified_iso": None}
    try:
        st = p.stat()
        from datetime import datetime, timezone

        return {
            "exists": True,
            "size_bytes": st.st_size,
            "modified_iso": datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat(),
        }
    except OSError:
        return {"exists": False, "size_bytes": 0, "modified_iso": None}


def build_health_deep() -> dict[str, Any]:
    root = get_repo_root()
    oc = openclaw_json_path()
    openclaw_ok = False
    openclaw_err = None
    if oc.is_file():
        txt = read_capped_text(oc)
        if txt is None:
            openclaw_err = "too_large"
        else:
            try:
                json.loads(txt)
                openclaw_ok = True
            except json.JSONDecodeError as e:
                _log.warning("health/deep: openclaw.json no parseable: %s", e)
                openclaw_err = "json_invalid"

    st = state_dir()
    act = activity_log_path()
    sync = run_sync_check()

    jd = judge_dir()
    judge_meta: dict[str, Any] = {"path": str(jd), "exists": jd.is_dir(), "file_count": 0}
    if jd.is_dir():
        try:
            judge_meta["file_count"] = sum(1 for _ in jd.iterdir())
        except OSError:
            judge_meta["file_count"] = 0

    td = tasks_dir()
    tasks_bytes, tasks_n = _dir_bytes(td, 2000)

    return {
        "repo_root": str(root),
        "openclaw_json": {"path": str(oc), "ok": openclaw_ok, "error": openclaw_err},
        "state_dir": str(st),
        "activity_log": _file_meta(act),
        "tasks_dir": {"path": str(td), "total_bytes_est": tasks_bytes, "files_scanned": tasks_n},
        "automations_sync": sync,
        "judge": judge_meta,
        "client_dossiers_bytes_est": _dir_bytes(client_dossiers_dir(), 500)[0],
        "automations_dir_exists": automations_dir().is_dir(),
        "env_JMC_STATE_DIR": bool(os.environ.get("JMC_STATE_DIR")),
    }
