#!/usr/bin/env bash
# Carga variables ClawFlows sin depender de la version exacta de Node en ~/.nvm/...
# Uso: source /home/will/jarvis-ecosystem/scripts/clawflows-env.sh

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export CLAWFLOWS_DIR="${CLAWFLOWS_DIR:-$ROOT/automations}"
export CLAWFLOWS_REGISTRY="${CLAWFLOWS_REGISTRY:-https://clawflows.com}"

NPM_GLOBAL="$(npm root -g 2>/dev/null)"
if [[ -n "$NPM_GLOBAL" && -d "$NPM_GLOBAL/openclaw/skills" ]]; then
  OC_SKILLS="$NPM_GLOBAL/openclaw/skills"
else
  OC_SKILLS=""
fi
JARVIS_SKILLS="$ROOT/agents/jarvis/skills"
if [[ -n "$OC_SKILLS" ]]; then
  export CLAWFLOWS_SKILLS="${OC_SKILLS}:${JARVIS_SKILLS}"
else
  export CLAWFLOWS_SKILLS="${JARVIS_SKILLS}"
fi
