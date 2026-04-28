#!/usr/bin/env bash
# Copia YAML canonicos desde automations/<empresa>/ hacia la raiz automations/
# para que `clawflows list` los detecte (el CLI solo lista *.yaml directos bajo CLAWFLOWS_DIR).
#
# Origen canónico: subcarpetas jarvis/, marketing/, ventas/, shared/
# Destino: raiz con nombre prefijado (ej. jarvis-morning-briefing.yaml).
#
# Uso (desde jarvis-ecosystem):
#   ./scripts/sync-automations-yaml.sh           # copia si hay diferencias
#   ./scripts/sync-automations-yaml.sh --check # solo diff, exit 1 si drift
#
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AUTO="$ROOT/automations"
CHECK_ONLY=false
[[ "${1:-}" == "--check" ]] && CHECK_ONLY=true

sync_pair() {
  local src_rel="$1"
  local dst_name="$2"
  local src="$AUTO/$src_rel"
  local dst="$AUTO/$dst_name"
  [[ -f "$src" ]] || { echo "ERROR: falta origen: $src" >&2; exit 1; }
  if [[ ! -f "$dst" ]] || ! cmp -s "$src" "$dst"; then
    if $CHECK_ONLY; then
      echo "DRIFT: $src_rel -> $dst_name"
      return 2
    fi
    cp "$src" "$dst"
    echo "OK: actualizado $dst_name <- $src_rel"
  else
    echo "OK: ya alineado $dst_name"
  fi
}

DRIFT=0
sync_pair "jarvis/morning-briefing.yaml" "jarvis-morning-briefing.yaml" || DRIFT=1
sync_pair "jarvis/coordination-pulse.yaml" "jarvis-coordination-pulse.yaml" || DRIFT=1
sync_pair "jarvis/loop-orchestrator.yaml" "jarvis-loop-orchestrator.yaml" || DRIFT=1
sync_pair "marketing/competitor-monitor.yaml" "marketing-competitor-monitor.yaml" || DRIFT=1
sync_pair "marketing/content-production-pipeline.yaml" "marketing-content-production-pipeline.yaml" || DRIFT=1
sync_pair "marketing/youtube-trending-watch.yaml" "marketing-youtube-trending-watch.yaml" || DRIFT=1
sync_pair "ventas/pipeline-report.yaml" "ventas-pipeline-report.yaml" || DRIFT=1
sync_pair "shared/security-audit.yaml" "shared-security-audit.yaml" || DRIFT=1

if [[ "$DRIFT" -ne 0 ]] && $CHECK_ONLY; then
  echo "ERROR: hay drift subcarpeta vs raiz. Ejecuta sin --check para copiar." >&2
  exit 1
fi
echo "Listo."
