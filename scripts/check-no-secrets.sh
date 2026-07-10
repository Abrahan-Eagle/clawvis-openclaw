#!/usr/bin/env bash
# Falla si archivos TRACKED por git contienen patrones de secretos de alto riesgo.
# No escanea runtime local ignorado (identity/, credentials/, .env en disco, venvs).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python3 - <<'PY'
import re
import subprocess
import sys
from pathlib import Path

patterns = [
    (re.compile(rb"sk-or-v1-[A-Za-z0-9]{20,}"), "OpenRouter API key"),
    (re.compile(rb"sk-[A-Za-z0-9]{32,}"), "OpenAI-style sk- key"),
    (re.compile(rb"xox[baprs]-[A-Za-z0-9-]{20,}"), "Slack token"),
    (re.compile(rb"ghp_[A-Za-z0-9]{30,}"), "GitHub PAT"),
    (re.compile(rb"-----BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY-----"), "Private key PEM"),
]

# Placeholders / valores cortos permitidos no disparan sk-or (requiere 20+ chars tras prefijo)

files = subprocess.check_output(
    ["git", "ls-files", "-z"], text=False
).split(b"\0")

hits = []
for raw in files:
    if not raw:
        continue
    path = Path(raw.decode("utf-8", errors="surrogateescape"))
    if not path.is_file():
        continue
    if path.name == "check-no-secrets.sh":
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
