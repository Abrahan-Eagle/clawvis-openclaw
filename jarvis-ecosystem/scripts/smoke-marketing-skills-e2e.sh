#!/usr/bin/env bash
# Smoke E2E marketing: activity-log + copy.md demo + handoff copy-to-design + coordinator status + end.
# Requiere dossier existente (ej. client-dossiers/cli-DEMO-rrss/).
#
# Uso (desde la raíz jarvis-ecosystem):
#   ./scripts/smoke-marketing-skills-e2e.sh
#
# Variables opcionales:
#   SMOKE_DOSSIER_ID   default: cli-DEMO-rrss

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

DOSSIER_ID="${SMOKE_DOSSIER_ID:-cli-DEMO-rrss}"
ACTIVITY="$ROOT/skills/global/activity-log/bin/activity-log"
HANDOFF="$ROOT/skills/global/handoff/bin/handoff"
COORD="$ROOT/skills/global/coordinator/bin/coordinator"

TASK_JSON=$("$ACTIVITY" start --agent mkt-content --title "Smoke IG 5 errores marketing" --dossier "$DOSSIER_ID" --ref copy)
TASK_ID=$(echo "$TASK_JSON" | jq -r '.task_id')
echo "task_id=$TASK_ID"

"$ACTIVITY" event --task "$TASK_ID" --agent mkt-content --kind milestone --note "Copy borrador smoke"

OUT_DIR="$ROOT/out/AGENCIA-TEST-2026-04-28/$DOSSIER_ID"
mkdir -p "$OUT_DIR"
cat > "$OUT_DIR/copy.md" << 'EOF'
# Post IG — 5 errores de marketing (demo smoke)

**Hook:** Los equipos que más crecen no publican más; evitan estos 5 errores.

1. Métricas de vanidad vs negocio.
2. Copy genérico sin prueba.
3. Demasiados CTAs en la misma vista.
4. IA en assets sin revisión (AG-13).
5. Publicar sin `marketing-context.md` en el dossier.

**CTA:** Revisá el dossier antes del próximo carrusel.
EOF

PAYLOAD="$(mktemp)"
trap 'rm -f "$PAYLOAD"' EXIT
cat > "$PAYLOAD" << EOF
{
  "hook": "5 errores de marketing que hoy siguen costando ventas",
  "slides": [
    "Error 1: métricas de vanidad",
    "Error 2: copy genérico",
    "Error 3: demasiados CTAs",
    "Error 4: IA sin revisión (AG-13)",
    "Error 5: sin dossier / marketing-context"
  ],
  "cta": "Revisá marketing-context.md antes del próximo asset.",
  "deliverable_format": "carousel_ig_1080x1350",
  "brand_id": "${DOSSIER_ID}"
}
EOF

HAND_JSON=$("$HANDOFF" create --from mkt-content --to design --schema copy-to-design --task "$TASK_ID" --payload-file "$PAYLOAD")
echo "$HAND_JSON"

"$COORD" status | head -80

"$ACTIVITY" end --task "$TASK_ID" --note "Smoke E2E marketing skills v2 OK"
echo "OK smoke E2E. Nota: puede WARN al cerrar si el handoff sigue abierto (aceptar con handoff accept antes del end para evitarlo)."
