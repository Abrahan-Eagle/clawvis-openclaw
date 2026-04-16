#!/usr/bin/env bash
# Sincroniza agents/jarvis/skills desde ESTE clon del repo hacia el workspace que usa OpenClaw.
# Uso tipico (host del gateway):
#   JARVIS_WORKSPACE_BASE=/home/aipp/jarvis-ecosystem \
#     /ruta/al/clawvis-openclaw/jarvis-ecosystem/scripts/sync-jarvis-skills-from-repo.sh
# Por defecto JARVIS_WORKSPACE_BASE=$HOME/jarvis-ecosystem
# Ver: jarvis-ecosystem/docs/COHERENCIA_RUNTIME_REPO.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
JARVIS_ECOSYSTEM="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC_SKILLS="$JARVIS_ECOSYSTEM/agents/jarvis/skills"
DEST_BASE="${JARVIS_WORKSPACE_BASE:-$HOME/jarvis-ecosystem}"
DEST_SKILLS="$DEST_BASE/agents/jarvis/skills"

if [[ ! -d "$SRC_SKILLS" ]]; then
  echo "ERROR: no existe origen: $SRC_SKILLS" >&2
  exit 1
fi

mkdir -p "$DEST_SKILLS"
rsync -a "$SRC_SKILLS/" "$DEST_SKILLS/"

if [[ -f "$DEST_SKILLS/carousel-ops/SKILL.md" ]]; then
  echo "OK: sincronizado. carousel-ops -> $DEST_SKILLS/carousel-ops/SKILL.md"
else
  echo "ADVERTENCIA: carousel-ops no aparece tras rsync (revisar permisos o origen)." >&2
  exit 1
fi
