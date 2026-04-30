"""Modo efectivo JARVIS_AUTONOMY_MODE + MEMORY.md autonomy_mode."""

from __future__ import annotations

import os
import re
from pathlib import Path

from app.security import allowed_path
from app.services.paths import docs_dir, repo_root
from app.services.read_capped import read_capped_text

_MD_MAX = 2 * 1024 * 1024
_MEMORY_MD_MAX = 512_000


def mode_write_enabled() -> bool:
    """Siempre activo: el Bearer token ya protege POST /v1/modes/current (escritura .env + os.environ)."""
    return True


_MODE_PHRASES = {
    "D": "Máximo control: cada gate AG pasa por solicitud explícita al CEO como hasta ahora.",
    "C": (
        "Trabajo solo en research y borradores locales; cualquier cosa visible fuera "
        "(RRSS, mails masivos, publicar) la consulto por Telegram/WhatsApp antes."
    ),
    "B": (
        "Como C, y además puedo automatizar pasos repetibles de bajo riesgo dentro del "
        "dossier que ya aprobaste (sin publicar al mundo sin tu OK)."
    ),
    "A": (
        "Piloto: máxima autonomía solo en horario y cuentas/rutas en lista blanca; "
        "fuera de eso aplico reglas tipo C o D."
    ),
}


def canonical_mode_phrases() -> dict[str, str]:
    """Frases UI por modo (A/B/C/D)."""
    return dict(_MODE_PHRASES)


_AUTONOMY_LINE = re.compile(
    r"^\s*autonomy_mode\s*:\s*([ABCD])\s*$",
    re.MULTILINE | re.IGNORECASE,
)


def _scan_memory_modes() -> dict[str, str]:
    out: dict[str, str] = {}
    agents_dir = repo_root() / "agents"
    if not agents_dir.is_dir():
        return out
    roots = (repo_root().resolve(),)
    for mem in agents_dir.rglob("MEMORY.md"):
        if not allowed_path(mem, roots):
            continue
        txt = read_capped_text(mem, max_bytes=_MEMORY_MD_MAX)
        if not txt:
            continue
        m = _AUTONOMY_LINE.search(txt)
        if not m:
            continue
        rel = str(mem.relative_to(repo_root()))
        out[rel] = m.group(1).upper()
    return out


def resolve_current_mode() -> dict:
    env_mode = os.environ.get("JARVIS_AUTONOMY_MODE", "").strip().upper()
    memory_modes = _scan_memory_modes()
    warnings: list[str] = []

    if env_mode and env_mode not in _MODE_PHRASES:
        warnings.append(f"JARVIS_AUTONOMY_MODE={env_mode!r} no reconocido; se ignora para modo efectivo")

    if env_mode in _MODE_PHRASES:
        effective = env_mode
    else:
        vals = set(memory_modes.values())
        if len(vals) == 1:
            effective = next(iter(vals))
        elif len(vals) > 1:
            effective = "D"
            warnings.append("Varios autonomy_mode distintos en MEMORY.md; mostrando D")
        else:
            effective = "D"
            warnings.append("Sin JARVIS_AUTONOMY_MODE válido ni autonomy_mode en MEMORY; asumiendo D")

    return {
        "effective_mode": effective,
        "phrase": _MODE_PHRASES.get(effective, _MODE_PHRASES["D"]),
        "env_mode": env_mode or None,
        "memory_modes": memory_modes,
        "doc_ref": "docs/AUTONOMIA_MODOS.md",
        "warnings": warnings,
    }


def parse_ag_modo_matrix() -> tuple[list[dict[str, str]], list[str]]:
    """
    Parsea la tabla 'Matriz AG × Modo' de docs/AUTONOMIA_MODOS.md.
    Retorna filas {gate_id, label, D, C, B, A} y warnings.
    """
    path = docs_dir() / "AUTONOMIA_MODOS.md"
    warnings: list[str] = []
    if not path.is_file():
        return [], ["AUTONOMIA_MODOS.md no encontrado"]

    text = read_capped_text(path, max_bytes=_MD_MAX)
    if text is None:
        return [], ["AUTONOMIA_MODOS.md no legible o supera tamaño máximo para el adapter"]
    rows: list[dict[str, str]] = []
    in_matrix = False
    for line in text.splitlines():
        ls = line.strip()
        if "| Gate |" in ls and "| D |" in ls:
            in_matrix = True
            continue
        if in_matrix and (ls.startswith("|---") or ls.startswith("|----")):
            continue
        if in_matrix and ls.startswith("|") and re.search(r"\bAG-\d+", ls):
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if len(parts) < 5:
                continue
            first = parts[0].strip()
            # Acepta "AG-10 Destructivo", "`AG-10` foo", o solo "AG-10" (sin texto tras el id)
            gid_m = re.search(r"(AG-\d+)", first)
            if not gid_m:
                continue
            gid = gid_m.group(1)
            rest = first[gid_m.end() :].strip()
            for strip_ch in ("`", "*", "_", "-", ":", "|"):
                rest = rest.lstrip(strip_ch).strip()
            label = rest or gid
            rows.append(
                {
                    "gate_id": gid,
                    "label": label,
                    "D": parts[1],
                    "C": parts[2],
                    "B": parts[3],
                    "A": parts[4],
                }
            )
            continue
        if in_matrix and ls and not ls.startswith("|"):
            break

    if not rows:
        warnings.append("Matriz AG × Modo vacía o formato cambió (¿backticks en Gate?)")
    return rows, warnings
