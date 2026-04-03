#!/usr/bin/env bash
# Enruta un turno local: elige agente según model-router.rules.yaml y ejecuta openclaw agent.
# No intercepta Telegram/Discord; solo CLI o automatizaciones.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MSG="${*:-}"
if [[ -z "${MSG// }" ]]; then
  echo "Uso: jarvis-agent-routed.sh <mensaje>" >&2
  exit 2
fi
JSON=$(node "$DIR/model-router.mjs" --json "$MSG")
AGENT=$(printf '%s' "$JSON" | node -e "process.stdout.write(JSON.parse(require('fs').readFileSync(0,'utf8')).agentId)")
if [[ "${JARVIS_ROUTER_VERBOSE:-}" == "1" ]]; then
  printf '%s\n' "$JSON" >&2
fi
exec openclaw agent --agent "$AGENT" -m "$MSG"
