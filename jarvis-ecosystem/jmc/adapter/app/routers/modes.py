"""Rutas /v1/modes/*."""

from __future__ import annotations

import logging
import os

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from app.security import require_token
from app.services.mode_writer import write_mode_to_env_file
from app.services.modes_resolver import (
    _MODE_PHRASES,
    canonical_mode_phrases,
    mode_write_enabled,
    parse_ag_modo_matrix,
    resolve_current_mode,
)
from app.services.paths import docs_dir
from app.services.read_capped import read_capped_text
from app.util_response import envelope

router = APIRouter(prefix="/modes", dependencies=[Depends(require_token)])
_log = logging.getLogger(__name__)


class ModeUpdate(BaseModel):
    """Cuerpo POST /v1/modes/current: solo el campo mode (A–D)."""

    model_config = ConfigDict(extra="forbid")
    mode: str = Field(..., min_length=1, max_length=8)


def _autonomia_table_md() -> str:
    p = docs_dir() / "AUTONOMIA_MODOS.md"
    if not p.is_file():
        return ""
    txt = read_capped_text(p, max_bytes=512_000)
    return txt or ""


@router.get("/matrix")
def modes_matrix():
    rows, warns = parse_ag_modo_matrix()
    return envelope({"matrix": rows, "doc_ref": "docs/AUTONOMIA_MODOS.md"}, warnings=warns)


def _modes_payload() -> tuple[dict, list[str]]:
    resolved = resolve_current_mode()
    warnings = list(resolved.get("warnings") or [])
    payload = {k: v for k, v in resolved.items() if k != "warnings"}
    payload["mode_write_enabled"] = mode_write_enabled()
    payload["mode_phrases"] = canonical_mode_phrases()
    return payload, warnings


@router.get("/current")
def modes_current():
    payload, warnings = _modes_payload()
    return envelope(payload, warnings=warnings)


@router.post("/current")
def modes_current_post(body: ModeUpdate):
    """Actualiza os.environ y ~/.openclaw/.env (requiere Bearer)."""
    raw = body.mode
    mode = str(raw).strip().upper()
    if mode not in _MODE_PHRASES:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "invalid_mode",
                    "message": f"Modo {raw!r} no válido; use A, B, C o D.",
                }
            },
        )
    os.environ["JARVIS_AUTONOMY_MODE"] = mode
    try:
        write_mode_to_env_file(mode)
    except ValueError as e:
        _log.warning("POST /modes/current: invalid_env_path: %s", e, exc_info=True)
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "invalid_env_path",
                    "message": "La ruta del .env no es válida (debe estar bajo ~/.openclaw/).",
                }
            },
        ) from e
    except OSError as e:
        _log.exception("POST /modes/current: env_write_failed: %s", e)
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "env_write_failed",
                    "message": "No se pudo escribir el archivo .env.",
                }
            },
        ) from e
    out, warnings = _modes_payload()
    return envelope(out, warnings=warnings)


@router.get("/doc_fragment")
def modes_doc_fragment():
    """Referencia: primeras líneas de la tabla de modos (solo lectura)."""
    txt = _autonomia_table_md()
    snippet = "\n".join(txt.splitlines()[:45])
    return envelope({"snippet": snippet, "path": "docs/AUTONOMIA_MODOS.md"})
