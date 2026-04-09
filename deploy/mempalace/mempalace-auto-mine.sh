#!/usr/bin/env bash
# Auto-mine: sincroniza cambios del ecosistema y sesiones OpenClaw hacia MemPalace.
# Instalación: copiar a ~/.openclaw/hooks/mempalace-auto-mine.sh y chmod +x
# Config: ~/.config/mempalace/restore.env (ver restore.env.example)

set -euo pipefail

CFG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/mempalace"
if [[ -f "${CFG_DIR}/restore.env" ]]; then
  set -a
  # shellcheck source=/dev/null
  source "${CFG_DIR}/restore.env"
  set +a
fi

PALACE="${MEMPALACE_PALACE:-${HOME}/.mempalace/palace}"
SESSIONS_DIR="${OPENCLAW_SESSIONS:-${HOME}/.openclaw/agents/jarvis/sessions}"
STAMP_FILE="${MEMPALACE_STAMP:-${HOME}/.mempalace/.last-mine-stamp}"
MEMPALACE_BIN="$(command -v mempalace || true)"
LOG="${MEMPALACE_LOG:-${HOME}/.mempalace/auto-mine.log}"

log() { echo "[$(date -Iseconds)] $*" >> "$LOG"; }

if [[ -z "$MEMPALACE_BIN" ]]; then
  echo "mempalace no está en PATH (instalar: pipx install mempalace)" >&2
  exit 1
fi

mkdir -p "$(dirname "$STAMP_FILE")" "$(dirname "$LOG")" "$PALACE"

if [[ ! -d "$PALACE" ]]; then
  log "ERROR: palace no existe: $PALACE"
  exit 1
fi

CHANGED=0

if [[ -n "${JARVIS_ECOSYSTEM:-}" && -d "$JARVIS_ECOSYSTEM" && -f "$JARVIS_ECOSYSTEM/mempalace.yaml" ]]; then
  if [[ ! -f "$STAMP_FILE" ]] || find "$JARVIS_ECOSYSTEM" -newer "$STAMP_FILE" \( -name "*.md" -o -name "*.yaml" -o -name "*.yml" -o -name "*.json" \) \
      -not -path "*/.venv/*" -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | head -1 | grep -q .; then
    log "Mining ecosistema: $JARVIS_ECOSYSTEM"
    "$MEMPALACE_BIN" mine "$JARVIS_ECOSYSTEM" --wing jarvis --agent jarvis >> "$LOG" 2>&1 || true
    CHANGED=1
  fi
else
  log "SKIP mine ecosistema: JARVIS_ECOSYSTEM no definido o sin mempalace.yaml"
fi

if [[ -d "$SESSIONS_DIR" ]]; then
  TMP_MINE="${TMPDIR:-/tmp}/mempalace-session-mine-$$"
  mkdir -p "$TMP_MINE"
  NEW_SESSIONS=0
  shopt -s nullglob
  for f in "$SESSIONS_DIR"/*.jsonl; do
    if [[ ! -f "$STAMP_FILE" ]] || [[ "$f" -nt "$STAMP_FILE" ]]; then
      cp "$f" "$TMP_MINE/"
      NEW_SESSIONS=$((NEW_SESSIONS + 1))
    fi
  done
  shopt -u nullglob

  if [[ "$NEW_SESSIONS" -gt 0 ]]; then
    cat > "$TMP_MINE/mempalace.yaml" <<'YAML'
wing: jarvis_sessions
rooms:
- name: sessions
  description: OpenClaw agent sessions
- name: general
  description: Other files
YAML
    log "Mining $NEW_SESSIONS sesiones JSONL..."
    "$MEMPALACE_BIN" mine "$TMP_MINE" --mode convos --wing jarvis_sessions --agent jarvis >> "$LOG" 2>&1 || true
    CHANGED=1
  fi
  rm -rf "$TMP_MINE"
fi

if [[ "$CHANGED" -eq 1 ]]; then
  touch "$STAMP_FILE"
  log "Auto-mine completo."
else
  log "Sin cambios relevantes."
fi
