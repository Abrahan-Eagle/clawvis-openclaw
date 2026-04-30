"""Invoca scripts/cost-report.sh y normaliza salida a JSON (cache TTL)."""

from __future__ import annotations

import os
import re
import subprocess
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.services.paths import cost_report_script, repo_root

_CACHE_LOCK = threading.Lock()
_CACHE: dict[str, tuple[float, dict[str, Any]]] = {}
_TTL_SEC = 60.0
_INFLIGHT_LOCK = threading.Lock()
_INFLIGHT: dict[str, threading.Event] = {}


def _month_arg() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


def _parse_int_token(s: str) -> int | None:
    s = str(s).strip()
    if not s:
        return None
    nums = re.sub(r"[^\d]", "", s)
    if not nums:
        return None
    try:
        return int(nums)
    except ValueError:
        return None


def _parse_models_top_line(val: str) -> list[dict[str, Any]]:
    """Parse 'model(count), model2(count2)' from Modelos top line."""
    out: list[dict[str, Any]] = []
    for part in val.split(","):
        part = part.strip()
        m = re.match(r"^(.+?)\((\d+)\)\s*$", part)
        if m:
            out.append({"model": m.group(1).strip(), "count": int(m.group(2))})
    return out[:5]


def normalize_agent_metrics(raw: dict[str, str]) -> dict[str, Any]:
    """Convierte métricas en texto del cost-report a números / listas."""
    out: dict[str, Any] = {}
    for k, v in raw.items():
        kl = k.lower().replace(".", "")
        if "sesiones" in kl:
            out["sessions_active"] = _parse_int_token(v)
        elif "mensajes" in kl and "user" in kl:
            out["messages_user"] = _parse_int_token(v)
        elif "mensajes" in kl and "assistant" in kl:
            out["messages_assistant"] = _parse_int_token(v)
        elif "tokens" in kl and "total" in kl:
            out["tokens_total"] = _parse_int_token(v)
        elif "tokens" in kl and "in" in kl:
            out["tokens_in"] = _parse_int_token(v)
        elif "tokens" in kl and "out" in kl:
            out["tokens_out"] = _parse_int_token(v)
        elif "modelos" in kl or "modelos_top" in kl:
            out["top_models"] = _parse_models_top_line(v)
    return out


def build_cost_envelope(data: dict[str, Any], *, include_raw: bool) -> dict[str, Any]:
    """Copia de respuesta para API: agents_normalized y raw_tail opcional."""
    agents = data.get("agents") or {}
    normalized: dict[str, Any] = {}
    for name, metrics in agents.items():
        if isinstance(metrics, dict):
            normalized[name] = normalize_agent_metrics({str(k): str(v) for k, v in metrics.items()})
        else:
            normalized[name] = {}
    out = {**data, "agents_normalized": normalized}
    if not include_raw:
        out.pop("raw_tail", None)
    return out


def _parse_cost_report_text(text: str) -> dict[str, Any]:
    agents: dict[str, Any] = {}
    current: str | None = None
    block_re = re.compile(r"^---\s+(.+?)\s+---\s*$")
    kv_re = re.compile(r"^\s+([A-Za-z é í ó ú á É Í Ó Ú Á üñÑ%().]+):\s*(.+)$")

    for line in text.splitlines():
        m = block_re.match(line.strip())
        if m:
            current = m.group(1).strip()
            agents.setdefault(current, {})
            continue
        if current and kv_re.match(line):
            mm = kv_re.match(line)
            assert mm
            k = mm.group(1).strip().lower().replace(" ", "_")
            v = mm.group(2).strip()
            agents[current][k] = v

    total_tokens = None
    for line in text.splitlines():
        if "TOTAL tokens est." in line or "TOTAL tokens est.:" in line:
            nums = re.findall(r"[\d,]+", line)
            if nums:
                total_tokens = int(nums[0].replace(",", ""))
                break

    return {
        "agents": agents,
        "summary_line_total_tokens_est": total_tokens,
        "raw_tail": text[-2000:] if len(text) > 2000 else text,
    }


def run_cost_report(month: str | None = None, env: dict[str, str] | None = None) -> dict[str, Any]:
    month = month or _month_arg()
    script = cost_report_script()
    if not script.is_file():
        return {"error": "cost-report.sh no encontrado", "agents": {}, "month": month}

    root = repo_root()
    env_full = {**dict(os.environ), **(env or {})}
    try:
        proc = subprocess.run(
            ["bash", str(script), month],
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=120,
            env=env_full,
        )
    except subprocess.TimeoutExpired:
        return {"error": "cost_report_timeout", "agents": {}, "month": month}

    out = proc.stdout or ""
    if proc.returncode != 0 and "ERROR" in (proc.stderr or ""):
        return {
            "error": "cost_report_failed",
            "month": month,
            "agents": {},
        }

    parsed = _parse_cost_report_text(out)
    parsed["month"] = month
    parsed["exit_code"] = proc.returncode
    return parsed


def get_cost_report_cached(month: str | None = None, env: dict[str, str] | None = None) -> dict[str, Any]:
    month = month or _month_arg()
    key = month
    now = time.monotonic()
    with _CACHE_LOCK:
        hit = _CACHE.get(key)
        if hit and now - hit[0] < _TTL_SEC:
            return hit[1]

    with _INFLIGHT_LOCK:
        if key in _INFLIGHT:
            evt = _INFLIGHT[key]
            leader = False
        else:
            evt = threading.Event()
            _INFLIGHT[key] = evt
            leader = True

    if not leader:
        evt.wait()
        with _CACHE_LOCK:
            hit = _CACHE.get(key)
            if hit and time.monotonic() - hit[0] < _TTL_SEC:
                return hit[1]
        return run_cost_report(month=month, env=env)

    try:
        data = run_cost_report(month=month, env=env)
        with _CACHE_LOCK:
            _CACHE[key] = (time.monotonic(), data)
        return data
    finally:
        with _INFLIGHT_LOCK:
            _INFLIGHT.pop(key, None)
        evt.set()
