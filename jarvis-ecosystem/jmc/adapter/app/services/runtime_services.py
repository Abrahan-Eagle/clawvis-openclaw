"""Consulta read-only de systemd (y opcional PM2) para servicios en lista blanca."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from typing import Any


def _parse_csv_services() -> list[str]:
    raw = os.environ.get("JMC_RUNTIME_SERVICES", "").strip()
    if not raw:
        return []
    out = [x.strip() for x in raw.split(",") if x.strip()]
    return out[:20]


def _systemctl_show(unit: str) -> dict[str, Any] | None:
    try:
        proc = subprocess.run(
            [
                "systemctl",
                "show",
                unit,
                "--property=ActiveState,SubState,MainPID,MemoryCurrent",
                "--no-pager",
            ],
            capture_output=True,
            text=True,
            timeout=8,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    kv: dict[str, str] = {}
    for line in (proc.stdout or "").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            kv[k.strip()] = v.strip()
    mem_kb = None
    mc = kv.get("MemoryCurrent", "")
    if mc.isdigit():
        mem_kb = int(mc) // 1024
    pid = None
    mp = kv.get("MainPID", "")
    if mp.isdigit():
        pid = int(mp)
    return {
        "name": unit,
        "source": "systemd",
        "active": kv.get("ActiveState", ""),
        "sub_state": kv.get("SubState", ""),
        "pid": pid,
        "memory_kb": mem_kb,
    }


def _pm2_jlist() -> list[dict[str, Any]]:
    pm2 = shutil.which("pm2")
    if not pm2:
        return []
    try:
        proc = subprocess.run([pm2, "jlist"], capture_output=True, text=True, timeout=12)
    except (OSError, subprocess.TimeoutExpired):
        return []
    if proc.returncode != 0 or not (proc.stdout or "").strip():
        return []
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list):
        return []
    out: list[dict[str, Any]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or item.get("pm_id") or "")
        pm2_env = item.get("pm2_env") if isinstance(item.get("pm2_env"), dict) else {}
        st = pm2_env.get("status")
        monit = item.get("monit") if isinstance(item.get("monit"), dict) else {}
        mem = monit.get("memory")
        pid = item.get("pid")
        pid_int = None
        if isinstance(pid, int):
            pid_int = pid
        elif isinstance(pid, str) and pid.isdigit():
            pid_int = int(pid, 10)
        mem_kb = None
        if isinstance(mem, (int, float)):
            mem_kb = int(mem) // 1024
        out.append(
            {
                "name": name or "?",
                "source": "pm2",
                "active": str(st or item.get("status") or ""),
                "sub_state": "",
                "pid": pid_int,
                "memory_kb": mem_kb,
            }
        )
    return out


def journal_tail(unit: str, lines: int) -> dict[str, Any] | None:
    if os.environ.get("JMC_RUNTIME_LOGS", "").strip() not in ("1", "true", "yes"):
        return None
    units = set(_parse_csv_services())
    if unit not in units:
        return None
    lines = max(1, min(int(lines), 20))
    try:
        proc = subprocess.run(
            ["journalctl", "-u", unit, "-n", str(lines), "--no-pager"],
            capture_output=True,
            text=True,
            timeout=12,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return {"unit": unit, "lines": lines, "text": (proc.stdout or "")[-8000:]}


def load_runtime_services(journal_lines: int = 0) -> dict[str, Any]:
    units = _parse_csv_services()
    if not units:
        return {
            "services": [],
            "pm2": [],
            "note": "JMC_RUNTIME_SERVICES vacío — no se consulta systemd.",
        }
    jl = max(0, min(int(journal_lines), 20))
    services = []
    for u in units:
        row = _systemctl_show(u)
        if row:
            if jl > 0:
                j = journal_tail(u, jl)
                if j:
                    row = {**row, "journal": j}
            services.append(row)
        else:
            base = {
                "name": u,
                "source": "systemd",
                "active": "unknown",
                "sub_state": "",
                "pid": None,
                "memory_kb": None,
            }
            if jl > 0:
                j = journal_tail(u, jl)
                if j:
                    base["journal"] = j
            services.append(base)
    pm2_rows = _pm2_jlist()
    return {"services": services, "pm2": pm2_rows}
