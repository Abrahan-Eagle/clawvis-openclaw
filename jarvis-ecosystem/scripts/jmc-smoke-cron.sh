#!/usr/bin/env bash
# Cron local opcional (v1.10): ejecuta jmc-smoke y anota fecha + código de salida.
# Crontab ejemplo: 0 * * * * /ruta/jarvis-ecosystem/scripts/jmc-smoke-cron.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/jmc"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/smoke.log"
{
  echo "$(date -Iseconds) start jmc-smoke"
  if bash "$ROOT/scripts/jmc-smoke.sh"; then
    echo "$(date -Iseconds) OK exit=0"
  else
    ec=$?
    echo "$(date -Iseconds) FAIL exit=$ec"
    exit "$ec"
  fi
} >>"$LOG" 2>&1
