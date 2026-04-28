#!/usr/bin/env bash
# Sincroniza agents/marketing/skills desde ESTE clon del repo hacia el workspace que usa OpenClaw (gateway).
# Paralelo a sync-jarvis-skills-from-repo.sh — necesario para que los agentes mkt-* vean las 40 skills profundas.
#
# Uso típico (host del gateway):
#   JARVIS_WORKSPACE_BASE=/home/aipp/jarvis-ecosystem \
#     /ruta/al/clawvis-openclaw/jarvis-ecosystem/scripts/sync-marketing-skills-from-repo.sh
# Por defecto JARVIS_WORKSPACE_BASE=$HOME/jarvis-ecosystem
# Ver: jarvis-ecosystem/docs/COHERENCIA_RUNTIME_REPO.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
JARVIS_ECOSYSTEM="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC_SKILLS="$JARVIS_ECOSYSTEM/agents/marketing/skills"
DEST_BASE="${JARVIS_WORKSPACE_BASE:-$HOME/jarvis-ecosystem}"
DEST_SKILLS="$DEST_BASE/agents/marketing/skills"

if [[ ! -d "$SRC_SKILLS" ]]; then
  echo "ERROR: no existe origen: $SRC_SKILLS" >&2
  exit 1
fi

mkdir -p "$DEST_SKILLS"
rsync -a "$SRC_SKILLS/" "$DEST_SKILLS/"

if [[ -f "$DEST_SKILLS/copywriting/SKILL.md" ]]; then
  echo "OK: sincronizado marketing skills -> $DEST_SKILLS/copywriting/SKILL.md"
else
  echo "ADVERTENCIA: copywriting/SKILL.md no aparece tras rsync (revisar permisos o origen)." >&2
  exit 1
fi
