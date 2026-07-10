#!/usr/bin/env bash
# Falla si archivos TRACKED por git contienen patrones de secretos de alto riesgo.
# No escanea runtime local ignorado (identity/, credentials/, .env en disco, venvs).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v git >/dev/null 2>&1; then
  echo "FAIL: git no está en PATH (necesario para listar archivos trackeados)." >&2
  exit 2
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "FAIL: python3 no está en PATH." >&2
  exit 2
fi

python3 - <<'PY'
import re
import subprocess
import sys
from pathlib import Path

# Patrones de alto riesgo (valores reales). Placeholders cortos no coinciden.
patterns = [
    (re.compile(rb"sk-or-v1-[A-Za-z0-9]{20,}"), "OpenRouter API key"),
    (re.compile(rb"sk-proj-[A-Za-z0-9_-]{20,}"), "OpenAI project key"),
    (re.compile(rb"sk-ant-[A-Za-z0-9_-]{20,}"), "Anthropic API key"),
    # OpenAI-style: sk- + al menos 32 alfanum (evita sk-proj- ya cubierto; no exige guiones)
    (re.compile(rb"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9]{32,}"), "OpenAI-style sk- key"),
    (re.compile(rb"xox[baprs]-[A-Za-z0-9-]{20,}"), "Slack token"),
    (re.compile(rb"gh[pousr]_[A-Za-z0-9]{30,}"), "GitHub token"),
    (re.compile(rb"gsk_[A-Za-z0-9]{20,}"), "Groq API key"),
    (re.compile(rb"AIza[0-9A-Za-z_-]{35}"), "Google API key"),
    # Telegram bot: 8–10 digits : AA… (35+ chars)
    (re.compile(rb"(?<![0-9])[0-9]{8,10}:AA[A-Za-z0-9_-]{30,}"), "Telegram bot token"),
    # Discord bot-ish tokens (base64-ish segments)
    (re.compile(rb"(?<![A-Za-z0-9_-])[MN][A-Za-z0-9_-]{23,}\.[A-Za-z0-9_-]{6}\.[A-Za-z0-9_-]{27,}"), "Discord-like token"),
    (re.compile(rb"-----BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY-----"), "Private key PEM"),
    # OpenClaw paired devices often store operator tokens as opaque strings in JSON
    (re.compile(rb'"tokens"\s*:\s*\{\s*"operator"\s*:\s*\{\s*"token"\s*:\s*"[^"]{16,}"'), "OpenClaw operator token"),
]

skip_names = {
    "check-no-secrets.sh",
    "pnpm-lock.yaml",
    "package-lock.json",
    "yarn.lock",
    "Cargo.lock",
    "poetry.lock",
    "INFORME_FORENSE_360_2026-07.md",  # documenta patrones, no secretos
}
skip_suffixes = (
    ".dist-info/RECORD",
    "/RECORD",
)

try:
    files = subprocess.check_output(
        ["git", "ls-files", "-z"],
        stderr=subprocess.PIPE,
    ).split(b"\0")
except subprocess.CalledProcessError as e:
    print("FAIL: no se pudo ejecutar git ls-files:", e.stderr.decode(errors="replace"), file=sys.stderr)
    sys.exit(2)
except FileNotFoundError:
    print("FAIL: git no encontrado.", file=sys.stderr)
    sys.exit(2)

hits = []
for raw in files:
    if not raw:
        continue
    path = Path(raw.decode("utf-8", errors="surrogateescape"))
    if not path.is_file():
        continue
    if path.name in skip_names:
        continue
    posix = path.as_posix()
    if any(posix.endswith(suf) or suf in posix for suf in skip_suffixes):
        continue
    if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4", ".sqlite", ".bin", ".woff", ".woff2", ".ttf", ".otf", ".pyc", ".wasm"}:
        continue
    try:
        data = path.read_bytes()
    except OSError:
        continue
    for pat, label in patterns:
        if pat.search(data):
            hits.append(f"{path}: {label}")
            break

if hits:
    print("FAIL: posibles secretos en archivos trackeados por git:", file=sys.stderr)
    for h in hits:
        print(f"  - {h}", file=sys.stderr)
    print(
        "\nUsa placeholders (OPENROUTER_API_KEY, etc.) y guarda valores reales solo en ~/.openclaw/.env",
        file=sys.stderr,
    )
    sys.exit(1)

print("OK: no se detectaron patrones de secretos de alto riesgo en archivos trackeados.")
PY
