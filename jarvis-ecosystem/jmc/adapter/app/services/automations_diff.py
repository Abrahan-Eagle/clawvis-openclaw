"""Estado sync automations: YAML raíz vs subcarpetas (subprocess --check)."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import yaml

from app.security import allowed_path
from app.services.paths import automations_dir, repo_root, sync_automations_script
from app.services.read_capped import read_capped_text


def _automations_root_rel() -> str:
    root = automations_dir()
    try:
        return str(root.resolve().relative_to(repo_root().resolve()))
    except ValueError:
        return "automations"


def _clip_out(s: str | None, n: int = 400) -> str:
    if not s:
        return ""
    t = str(s).strip()
    return t if len(t) <= n else t[:n] + "…[truncated]"


def list_automation_yamls() -> dict[str, Any]:
    root = automations_dir()
    root_rel = _automations_root_rel()
    if not root.is_dir():
        return {"root": root_rel, "files": [], "nested": []}

    roots = (repo_root().resolve(),)
    files = sorted(
        p.name for p in root.glob("*.yaml") if allowed_path(p, roots) and p.is_file()
    )
    nested = sorted(
        str(p.relative_to(root))
        for p in root.rglob("*.yaml")
        if p.parent != root and allowed_path(p, roots) and p.is_file()
    )
    return {"root": root_rel, "files": files, "nested": nested}


def load_yaml_preview(max_files: int = 40) -> dict[str, Any]:
    root = automations_dir()
    previews: dict[str, Any] = {}
    if not root.is_dir():
        return previews
    roots = (repo_root().resolve(),)
    for i, p in enumerate(sorted(root.rglob("*.yaml"))):
        if i >= max_files:
            previews["__truncated__"] = True
            break
        if not allowed_path(p, roots):
            continue
        rel = str(p.relative_to(repo_root()))
        text = read_capped_text(p)
        if text is None:
            previews[rel] = {"error": "too_large"}
            continue
        try:
            data = yaml.safe_load(text) or {}
            previews[rel] = {
                "keys": list(data.keys()) if isinstance(data, dict) else type(data).__name__,
            }
        except yaml.YAMLError:
            previews[rel] = {
                "error": "No se pudo leer o parsear el YAML (detalle en logs del servidor).",
            }
    return previews


def run_sync_check() -> dict[str, Any]:
    script = sync_automations_script()
    if not script.is_file():
        return {"ok": False, "error": "sync script missing", "stdout": "", "stderr": ""}

    proc = subprocess.run(
        ["bash", str(script), "--check"],
        cwd=str(repo_root()),
        capture_output=True,
        text=True,
        timeout=60,
    )
    return {
        "ok": proc.returncode == 0,
        "exit_code": proc.returncode,
        "stdout": _clip_out(proc.stdout, 800),
        "stderr": _clip_out(proc.stderr, 800),
    }
