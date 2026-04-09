#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${MEMPALACE_PYTHON:-${HOME}/.local/share/pipx/venvs/mempalace/bin/python3}"
if [[ ! -x "$PY" ]]; then
  echo "No se encontró Python del venv pipx en: $PY" >&2
  echo "Exporte MEMPALACE_PYTHON=/ruta/al/python3 del venv mempalace" >&2
  exit 1
fi
exec "$PY" "${SCRIPT_DIR}/kg-populate-ecosystem.py" "$@"
