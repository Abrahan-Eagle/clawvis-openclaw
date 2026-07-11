#!/usr/bin/env bash
# marketing-dispatch.sh — convierte handoffs abiertos hacia mkt-* en agentTurn / system event
# No publica. Respeta AG-12/13 (solo despacha trabajo; el agente debe pedir gate).
set -euo pipefail

usage() {
  cat <<'EOF'
marketing-dispatch.sh [--dry-run] [--agent ID] [--max N] [--min-age-minutes M]

Lee handoffs abiertos (sin accept/reject) cuyo --to es un agente mkt-*.
Por cada uno dispara un turno OpenClaw (system event o cron one-shot) y registra
activity-log event --kind dispatch.

Opciones:
  --dry-run            Solo lista qué se despacharía (default si OPENCLAW no está)
  --agent ID           Solo handoffs hacia ese agentId
  --max N              Máximo de despachos en esta corrida (default 5)
  --min-age-minutes M  Ignorar handoffs más nuevos que M minutos (default 0)

Variables:
  JARVIS_STATE_DIR     Override de state/
  MARKETING_DISPATCH_MODE=dry-run|event|cron  (default: event si openclaw en PATH, else dry-run)
EOF
}

detect_root() {
  local r
  if r=$(git rev-parse --show-toplevel 2>/dev/null); then
    if [ -d "$r/jarvis-ecosystem" ]; then
      echo "$r/jarvis-ecosystem"
      return 0
    fi
    if [ -d "$r/state" ]; then
      echo "$r"
      return 0
    fi
  fi
  local self
  self=$(readlink -f "${BASH_SOURCE[0]}")
  cd "$(dirname "$self")/.." && pwd
}

ROOT=$(detect_root)
STATE_DIR="${JARVIS_STATE_DIR:-$ROOT/state}"
HANDOFFS_DIR="$STATE_DIR/handoffs"
ACTIVITY_LOG="$ROOT/skills/global/activity-log/bin/activity-log"
HANDOFF_BIN="$ROOT/skills/global/handoff/bin/handoff"

DRY_RUN=false
ONLY_AGENT=""
MAX=5
MIN_AGE=0
MODE="${MARKETING_DISPATCH_MODE:-}"

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    --agent) ONLY_AGENT="$2"; shift 2 ;;
    --max) MAX="$2"; shift 2 ;;
    --min-age-minutes) MIN_AGE="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Opcion desconocida: $1" >&2; usage; exit 1 ;;
  esac
done

MKT_AGENTS='mkt-content|mkt-social|mkt-analytics|mkt-ads|mkt-email|mkt-research'

if [ -z "$MODE" ]; then
  if command -v openclaw >/dev/null 2>&1; then
    MODE=event
  else
    MODE=dry-run
  fi
fi
if [ "$DRY_RUN" = true ]; then
  MODE=dry-run
fi

ts_now() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

age_minutes() {
  local created="$1"
  python3 -c "
from datetime import datetime, timezone
import sys
s=sys.argv[1].replace('Z','+00:00')
try:
  t=datetime.fromisoformat(s)
except Exception:
  print(99999); raise SystemExit
now=datetime.now(timezone.utc)
print(int((now-t).total_seconds()//60))
" "$created" 2>/dev/null || echo 99999
}

dispatch_one() {
  local agent="$1" hid="$2" schema="$3" task="$4"
  local msg
  msg=$(cat <<EOF
[marketing-dispatch] Handoff abierto $hid (schema=$schema, task=$task).
1) handoff list --open --to $agent
2) handoff accept --id $hid --by $agent (o reject con razon)
3) Ejecuta UNA unidad de trabajo del payload
4) Si asset listo para publicar: judge-run --handoff $hid (revisar state/judge/) LUEGO approval-gate request AG-12 y STOP (no publiques)
5) Si no hay mas trabajo: HEARTBEAT_OK
EOF
)

  case "$MODE" in
    dry-run)
      echo "DRY-RUN would dispatch agent=$agent handoff=$hid"
      ;;
    event)
      # system event despierta agentes con heartbeat; el texto guía al agente destino
      openclaw system event --text "$msg" --mode now || {
        echo "WARN: openclaw system event fallo; registrando solo log" >&2
      }
      ;;
    cron)
      # One-shot documentado: requiere openclaw cron add (API puede variar por versión)
      if openclaw cron --help >/dev/null 2>&1; then
        openclaw cron add --agent "$agent" --name "dispatch-$hid" --at now --message "$msg" 2>/dev/null \
          || openclaw system event --text "[agent:$agent] $msg" --mode now || true
      else
        openclaw system event --text "[agent:$agent] $msg" --mode now || true
      fi
      ;;
    *)
      echo "ERROR: MODE desconocido: $MODE" >&2
      return 1
      ;;
  esac

  if [ -x "$ACTIVITY_LOG" ]; then
    "$ACTIVITY_LOG" event \
      --agent jarvis \
      --task "${task:-dispatch}" \
      --kind dispatch \
      --payload "{\"handoff_id\":\"$hid\",\"to\":\"$agent\",\"schema\":\"$schema\",\"mode\":\"$MODE\"}" \
      >/dev/null 2>&1 || true
  fi
}

mkdir -p "$HANDOFFS_DIR"
count=0
shopt -s nullglob
for f in "$HANDOFFS_DIR"/handoff-*.json; do
  [ "$count" -ge "$MAX" ] && break
  row=$(jq -c '
    select(.accepted_at == null and .rejected_at == null)
    | {id, to, schema, task_id, created_at}
  ' "$f" 2>/dev/null || true)
  [ -z "$row" ] || [ "$row" = "null" ] && continue

  to=$(jq -r '.to' <<<"$row")
  echo "$to" | grep -Eq "^($MKT_AGENTS)$" || continue
  if [ -n "$ONLY_AGENT" ] && [ "$to" != "$ONLY_AGENT" ]; then
    continue
  fi

  created=$(jq -r '.created_at // empty' <<<"$row")
  if [ -n "$created" ] && [ "$MIN_AGE" -gt 0 ]; then
    am=$(age_minutes "$created")
    [ "$am" -lt "$MIN_AGE" ] && continue
  fi

  hid=$(jq -r '.id' <<<"$row")
  schema=$(jq -r '.schema' <<<"$row")
  task=$(jq -r '.task_id' <<<"$row")
  dispatch_one "$to" "$hid" "$schema" "$task"
  count=$((count + 1))
done

echo "{\"dispatched\":$count,\"mode\":\"$MODE\",\"ts\":\"$(ts_now)\"}"
