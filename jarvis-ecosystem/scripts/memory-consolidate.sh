#!/usr/bin/env bash
# memory-consolidate.sh — propone entradas para agents/<agent>/memory.json (HITL).
# Por defecto solo imprime; con --apply escribe vía memory-store set.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENT=""
APPLY=0
DAYS=14
MAX_LINES=40

usage() {
  cat <<'EOF'
Uso: scripts/memory-consolidate.sh --agent jarvis|marketing [--days N] [--apply]

Lee agents/<agent>/memory/*.md (recientes) + state/activity-log.jsonl y propone
claves para memory.json. Sin --apply solo imprime comandos sugeridos (HITL).
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent) AGENT="$2"; shift 2 ;;
    --days) DAYS="$2"; shift 2 ;;
    --apply) APPLY=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Opción desconocida: $1" >&2; usage; exit 1 ;;
  esac
done

[[ -n "$AGENT" ]] || { usage; exit 1; }
AGENT_DIR="$ROOT/agents/$AGENT"
MEM_JSON="$AGENT_DIR/memory.json"
MEM_DIR="$AGENT_DIR/memory"
LOG="$ROOT/state/activity-log.jsonl"
STORE="$ROOT/skills/global/memory-store/bin/memory-store"

[[ -d "$AGENT_DIR" ]] || { echo "ERROR: no existe $AGENT_DIR" >&2; exit 1; }
[[ -x "$STORE" ]] || { echo "ERROR: memory-store no ejecutable" >&2; exit 1; }

echo "# memory-consolidate — agent=$AGENT days=$DAYS apply=$APPLY"
echo "# Generado: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo

propose() {
  local cat="$1" key="$2" val="$3"
  echo "## propose notes/$key"
  echo "categoría=$cat clave=$key"
  echo "valor=$val"
  echo "cmd: memory-store --file $MEM_JSON set $cat $key $(printf '%q' "$val")"
  echo
  if [[ "$APPLY" -eq 1 ]]; then
    "$STORE" --file "$MEM_JSON" set "$cat" "$key" "$val"
    echo "(applied)"
    echo
  fi
}

# Daily memory snippets
if [[ -d "$MEM_DIR" ]]; then
  mapfile -t FILES < <(find "$MEM_DIR" -maxdepth 1 -name '*.md' -type f -mtime -"$DAYS" 2>/dev/null | sort | tail -n 8)
  idx=0
  for f in "${FILES[@]:-}"; do
    [[ -z "${f:-}" ]] && continue
    base=$(basename "$f" .md)
    snippet=$(head -n 12 "$f" | tr '\n' ' ' | sed 's/  */ /g' | cut -c1-320)
    [[ -z "$snippet" ]] && continue
    idx=$((idx + 1))
    propose "notes" "daily_${base}" "$snippet"
  done
fi

# Activity log signals
if [[ -f "$LOG" ]]; then
  echo "# Señales activity-log (últimas ${MAX_LINES} líneas relevantes)"
  mapfile -t LINES < <(tail -n 400 "$LOG" | grep -E '"type":"(block|reject|end|event)"|"kind":"(approval_request|handoff_reject|error)"' | tail -n "$MAX_LINES" || true)
  n=0
  for line in "${LINES[@]:-}"; do
    [[ -z "${line:-}" ]] && continue
    agent=$(echo "$line" | jq -r '.agent // empty' 2>/dev/null || true)
    typ=$(echo "$line" | jq -r '.type // .payload.kind // empty' 2>/dev/null || true)
    note=$(echo "$line" | jq -r '.payload.note // .payload.reason // .payload.title // empty' 2>/dev/null || true)
    [[ -z "$note" ]] && continue
    # Filtrar por agente si marketing/jarvis
    if [[ "$AGENT" == "marketing" && "$agent" != mkt-* && "$agent" != "marketing" ]]; then
      continue
    fi
    if [[ "$AGENT" == "jarvis" && "$agent" != "jarvis" && "$agent" != mkt-* ]]; then
      : # jarvis ve holding
    fi
    n=$((n + 1))
    key="log_$(echo "$typ" | tr -c 'A-Za-z0-9' '_')_$n"
    val=$(echo "[$agent/$typ] $note" | cut -c1-360)
    propose "notes" "$key" "$val"
    [[ "$n" -ge 5 ]] && break
  done
fi

# Seed hint from LESSONS if notes thin
if [[ -f "$ROOT/LESSONS.md" ]]; then
  echo "# Lecciones (referencia LESSONS.md — no auto-aplica filas; usar lessons-scan.sh)"
  echo "Ver: scripts/lessons-scan.sh"
  echo
fi

if [[ "$APPLY" -eq 0 ]]; then
  echo "# HITL: revisa propuestas. Para aplicar: $0 --agent $AGENT --apply"
  echo "# Luego: memory-store --file $MEM_JSON trim && memory-store --file $MEM_JSON format-prompt"
fi
