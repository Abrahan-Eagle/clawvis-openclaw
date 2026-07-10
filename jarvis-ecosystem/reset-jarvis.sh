#!/usr/bin/env bash
# Jarvis Reset Tool — limpia locks y procesos OpenClaw colgados (sin matar todo Node del host).
set -euo pipefail

echo "Iniciando limpieza de emergencia del Ecosistema Jarvis..."

# 1. Terminar solo procesos OpenClaw / gateway relacionados (no `pkill -f node` global)
echo "Terminando procesos OpenClaw (gateway / CLI)..."
pkill -f '[o]penclaw' 2>/dev/null || true
pkill -f '[o]penclaw-gateway' 2>/dev/null || true
# Cursor proxy del ecosistema (puerto 4646) — opcional
if [[ "${RESET_CURSOR_PROXY:-0}" == "1" ]]; then
  echo "Terminando cursor-agent-api-proxy (RESET_CURSOR_PROXY=1)..."
  pkill -f 'cursor-agent-api' 2>/dev/null || true
fi

# 2. Limpiar archivos de bloqueo (.lock) que impiden que Jarvis inicie
echo "Limpiando archivos de bloqueo (.lock)..."
rm -f "$HOME/.openclaw/agents/"*/sessions/*.lock 2>/dev/null || true

echo "Sistema desbloqueado."
echo "Siguiente paso tipico: systemctl --user restart openclaw-gateway"
echo "O: openclaw agent --agent jarvis --message \"ping\""
