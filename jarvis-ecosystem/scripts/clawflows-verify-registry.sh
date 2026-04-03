#!/usr/bin/env bash
# Ejecuta `clawflows check` sobre cada automatizacion instalada en automations/registry/
# Requisito: source scripts/clawflows-env.sh (o este script lo hace).

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=clawflows-env.sh
source "$ROOT/scripts/clawflows-env.sh"

REG="$ROOT/automations/registry"
FAILED=0

echo "=== ClawFlows: verificacion de registry (CLAWFLOWS_SKILLS) ==="
echo "$CLAWFLOWS_SKILLS"
echo ""

for f in "$REG"/*.yaml; do
  [[ -e "$f" ]] || continue
  base=$(basename "$f" .yaml)
  echo "---------- $base ----------"
  if [[ "$base" == "lead-qualifier" ]]; then
    echo "Omitido: clawflows check usa metadata remoto; lead-qualifier no tiene metadata.json en https://clawflows.com (404). El YAML local usa requires: curl/jq — validar manualmente."
    echo ""
    continue
  fi
  if ! clawflows check "$base" 2>&1; then
    FAILED=1
  fi
  echo ""
done

if [[ "$FAILED" -ne 0 ]]; then
  echo "Algunos checks fallaron. Revisa skills y CAPABILITY.md (clawflows-capability-map)." >&2
  exit 1
fi
echo "Listo: todos los checks soportados pasaron."
