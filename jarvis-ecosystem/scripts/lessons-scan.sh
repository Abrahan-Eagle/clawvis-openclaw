#!/usr/bin/env bash
# lessons-scan.sh — candidatos L0XX para LESSONS.md desde activity-log (HITL, solo imprime).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$ROOT/state/activity-log.jsonl"
TAIL_N=800

usage() {
  cat <<'EOF'
Uso: scripts/lessons-scan.sh [--log PATH] [--tail N]

Analiza activity-log.jsonl (rechazos, block, errores) y propone filas candidatas
para LESSONS.md en formato L0XX. Solo imprime; el CEO decide qué añadir.
Cadencia: cierre de módulo o semanal (session-learner-ops OVERLAY).
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --log) LOG="$2"; shift 2 ;;
    --tail) TAIL_N="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Opción: $1" >&2; usage; exit 1 ;;
  esac
done

[[ -f "$LOG" ]] || { echo "ERROR: no existe $LOG" >&2; exit 1; }

next_id=18
if [[ -f "$ROOT/LESSONS.md" ]]; then
  last=$(grep -oE 'L[0-9]{3}' "$ROOT/LESSONS.md" | sort -u | tail -1 || true)
  if [[ -n "$last" ]]; then
    num=${last#L}
    next_id=$((10#$num + 1))
  fi
fi

echo "# Candidatos LESSONS.md — $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "# Fuente: $LOG (últimas $TAIL_N líneas)"
echo "# HITL: copiar filas aprobadas a LESSONS.md; no auto-escribir."
echo
echo "| ID | Fecha | Error | Causa Raíz (propuesta) | Acción Correctiva / Prevención |"
echo "|---|---|---|---|---|"

tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT

tail -n "$TAIL_N" "$LOG" | while IFS= read -r line; do
  echo "$line" | jq -e . >/dev/null 2>&1 || continue
  typ=$(echo "$line" | jq -r '.type // empty')
  kind=$(echo "$line" | jq -r '.payload.kind // empty')
  reason=$(echo "$line" | jq -r '.payload.reason // .payload.note // empty')
  agent=$(echo "$line" | jq -r '.agent // empty')
  ts=$(echo "$line" | jq -r '.ts // empty' | cut -c1-10)

  interesting=0
  case "$typ" in block|reject) interesting=1 ;; esac
  case "$kind" in error|handoff_reject|approval_reject|escalation) interesting=1 ;; esac
  # Señales explícitas (evitar falsos positivos tipo "5-errores-marketing")
  echo "$reason" | grep -qiE '\brejected\b|\bfailed\b|\bschema\b|invalid|abort|AG-[0-9]+ pending|handoff reject' && interesting=1
  [[ "$interesting" -eq 1 ]] || continue
  [[ -n "$reason" ]] || reason="(sin note) type=$typ kind=$kind agent=$agent"
  key=$(echo "$reason" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '_' | cut -c1-80)
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$ts" "$agent" "$typ" "$kind" "$reason" "$key"
done > "$tmp"

i=0
while IFS=$'\t' read -r ts agent typ kind reason key; do
  [[ -z "${key:-}" ]] && continue
  id=$(printf 'L%03d' $((next_id + i)))
  i=$((i + 1))
  err=$(printf '[%s] %s/%s: %s' "$agent" "$typ" "$kind" "$reason" | cut -c1-120 | sed 's/|/\\|/g')
  echo "| $id | ${ts:-?} | $err | Revisar activity-log + schema/gate | Documentar en LESSONS; ajustar HEARTBEAT/skill si recurrente |"
  [[ "$i" -ge 12 ]] && break
done < <(awk -F'\t' '!seen[$6]++' "$tmp")

if [[ "$i" -eq 0 ]]; then
  echo "| (ninguno) | — | Sin señales fuertes en la ventana | — | Ampliar --tail o generar más eventos |"
fi

echo
echo "# Cadencia: cierre de módulo / semanal (session-learner-ops)."
echo "# Siguiente ID libre base: L$(printf '%03d' "$next_id")"
