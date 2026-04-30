#!/usr/bin/env bash
# Arranca el adapter JMC (API local: lectura de estado + escritura acotada de modo) en 127.0.0.1.
# Requiere: JMC_BEARER_TOKEN (>=32 chars). Opcional: JMC_BIND, JMC_PORT.
# Si JMC_BEARER_TOKEN no está en el shell, se intenta cargar (en orden) JMC_ENV_FILE,
# /etc/jmc/jmc-adapter.env, ~/.config/jmc/jmc-adapter.env — mismas rutas típicas que systemd.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/jmc/adapter"
export JMC_BIND="${JMC_BIND:-127.0.0.1}"
export JMC_PORT="${JMC_PORT:-8765}"
if [[ -z "${JMC_BEARER_TOKEN:-}" ]]; then
  for envf in "${JMC_ENV_FILE:-}" "/etc/jmc/jmc-adapter.env" "${HOME}/.config/jmc/jmc-adapter.env"; do
    [[ -z "$envf" ]] && continue
    if [[ -f "$envf" && -r "$envf" ]]; then
      set -a
      # shellcheck disable=SC1090
      source "$envf"
      set +a
      break
    fi
  done
fi
if [[ -z "${JMC_BEARER_TOKEN:-}" ]]; then
  echo "ERROR: falta JMC_BEARER_TOKEN (>=32 caracteres)." >&2
  echo "  export JMC_BEARER_TOKEN=...   o   crea /etc/jmc/jmc-adapter.env (sudo ./scripts/jmc-systemd-install.sh)." >&2
  echo "  Opcional: JMC_ENV_FILE=/ruta/al.env ./scripts/jmc-start.sh" >&2
  exit 1
fi
if [[ ${#JMC_BEARER_TOKEN} -lt 32 ]]; then
  echo "ERROR: JMC_BEARER_TOKEN debe tener al menos 32 caracteres (tiene ${#JMC_BEARER_TOKEN})." >&2
  exit 1
fi
UV="${ROOT}/.venv-jmc/bin/uvicorn"
if [[ ! -x "$UV" ]]; then
  UV="$(command -v uvicorn)"
fi
if [[ ! -x "$UV" ]]; then
  echo "ERROR: no hay uvicorn ejecutable. Crea el venv: cd \"$ROOT\" && python3 -m venv .venv-jmc && .venv-jmc/bin/pip install -e jmc/adapter" >&2
  exit 1
fi
PY="$(dirname "$UV")/python"
if ! (cd "$ROOT/jmc/adapter" && "$PY" -c "import app.main" 2>/dev/null); then
  echo "ERROR: el venv no tiene el adapter JMC instalado (falló import app.main). Ejecuta:" >&2
  echo "  cd \"$ROOT\" && .venv-jmc/bin/pip install -e jmc/adapter" >&2
  exit 1
fi
exec "$UV" app.main:app --host "$JMC_BIND" --port "$JMC_PORT" --workers 1
