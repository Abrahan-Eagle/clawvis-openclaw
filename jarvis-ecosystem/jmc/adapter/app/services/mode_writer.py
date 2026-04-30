"""Escritura opt-in de JARVIS_AUTONOMY_MODE en archivo .env (JMC v1.8)."""

from __future__ import annotations

import os
import stat
import tempfile
from pathlib import Path

from app.services.read_capped import read_capped_text

_LINE_KEY = "JARVIS_AUTONOMY_MODE"


def _openclaw_config_dir_resolved() -> Path:
    return (Path.home() / ".openclaw").resolve()


def _validated_env_file_path(p: Path) -> Path:
    """Solo rutas bajo ~/.openclaw/ (resolve + relative_to)."""
    allow = _openclaw_config_dir_resolved()
    try:
        rp = p.expanduser().resolve()
    except OSError as e:
        raise ValueError(f"No se pudo resolver la ruta del .env: {e}") from e
    try:
        rp.relative_to(allow)
    except ValueError:
        raise ValueError(
            "JMC_OPENCLAW_ENV_PATH debe apuntar a un fichero dentro de ~/.openclaw/"
        ) from None
    return rp


def resolve_openclaw_env_path() -> Path:
    """Ruta del .env a reescribir: JMC_OPENCLAW_ENV_PATH o ~/.openclaw/.env (validada)."""
    raw = os.environ.get("JMC_OPENCLAW_ENV_PATH", "").strip()
    target = Path(raw) if raw else Path.home() / ".openclaw" / ".env"
    return _validated_env_file_path(target)


def _build_env_body(p: Path, mode: str) -> str:
    new_line = f"{_LINE_KEY}={mode}\n"
    if not p.is_file():
        return new_line
    text = read_capped_text(p, max_bytes=128_000) or ""
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    found = False
    for line in lines:
        stripped = line.lstrip()
        if stripped.upper().startswith(f"{_LINE_KEY.upper()}=") or stripped.upper().startswith(
            f"{_LINE_KEY.upper()} ="
        ):
            if not found:
                out.append(new_line)
                found = True
            continue
        out.append(line)
    if not found:
        if out and not out[-1].endswith("\n"):
            out[-1] = out[-1] + "\n"
        out.append(new_line)
    return "".join(out)


def write_mode_to_env_file(mode: str, path: Path | None = None) -> Path:
    """
    Asegura JARVIS_AUTONOMY_MODE=<mode> en el archivo dado.
    Crea directorios si faltan; escritura atómica (temp + os.replace); chmod 0600 en archivo nuevo.
    """
    mode = mode.strip().upper()
    p = resolve_openclaw_env_path() if path is None else _validated_env_file_path(path)
    existed = p.is_file()
    body = _build_env_body(p, mode)
    p.parent.mkdir(parents=True, exist_ok=True)

    fd, tmp_name = tempfile.mkstemp(prefix=".jmc-env-", suffix=".tmp", dir=str(p.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as wf:
            wf.write(body)
        try:
            os.chmod(tmp_name, stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass
        os.replace(str(tmp_path), str(p))
    except Exception:
        try:
            tmp_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise
    if not existed:
        try:
            p.chmod(stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass
    return p
