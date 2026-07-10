#!/usr/bin/env bash
# Jarvis Reset Tool — limpia locks y procesos OpenClaw colgados (sin matar todo Node del host).
# No usa pkill genérico sobre "openclaw" (coincidiría con rutas del repo / este script).
set -euo pipefail

SELF_PID=$$
echo "Iniciando limpieza de emergencia del Ecosistema Jarvis..."

kill_matching() {
  local pattern="$1"
  local label="$2"
  local pids
  pids="$(pgrep -f "$pattern" 2>/dev/null || true)"
  if [[ -z "$pids" ]]; then
    echo "  (sin procesos: $label)"
    return 0
  fi
  for pid in $pids; do
    if [[ "$pid" == "$SELF_PID" ]] || [[ "$pid" == "$$" ]]; then
      continue
    fi
    # No matar el shell padre de esta invocación
    if [[ "$pid" == "$PPID" ]]; then
      continue
    fi
    echo "  kill $pid ($label)"
    kill "$pid" 2>/dev/null || true
  done
}

# 1. Terminar solo gateway / CLI OpenClaw (patrones específicos)
echo "Terminando procesos OpenClaw (gateway / CLI)..."
kill_matching 'openclaw-gateway' 'openclaw-gateway'
kill_matching 'openclaw/dist/index\.js' 'openclaw dist entry'
kill_matching 'openclaw.*gateway' 'openclaw gateway argv'
# CLI one-shots suelen morir solos; no matamos editores con "openclaw" en la ruta del cwd

# Cursor proxy del ecosistema (puerto 4646) — opcional
if [[ "${RESET_CURSOR_PROXY:-0}" == "1" ]]; then
  echo "Terminando cursor-agent-api-proxy (RESET_CURSOR_PROXY=1)..."
  kill_matching 'cursor-agent-api' 'cursor-agent-api'
fi

# 2. Limpiar archivos de bloqueo (.lock) que impiden que Jarvis inicie
echo "Limpiando archivos de bloqueo (.lock)..."
rm -f "$HOME/.openclaw/agents/"*/sessions/*.lock 2>/dev/null || true

echo "Sistema desbloqueado."
echo "Siguiente paso tipico: systemctl --user restart openclaw-gateway"
echo "O: openclaw agent --agent jarvis --message \"ping\""
