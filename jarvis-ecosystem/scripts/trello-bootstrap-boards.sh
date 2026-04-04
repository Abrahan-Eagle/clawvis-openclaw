#!/usr/bin/env bash
# Crea tableros Empresa-marketing / Empresa-ventas y listas Kanban según CONVENCION_TRELLO_EMPRESA_CLIENTE.md
# Requiere: TRELLO_API_KEY y TRELLO_TOKEN con permiso de ESCRITURA (trello.com/app-key → autorizar token).
set -euo pipefail
ENV_FILE="${OPENCLAW_ENV:-$HOME/.openclaw/.env}"
if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck source=/dev/null
  source "$ENV_FILE"
  set +a
fi
if [[ -z "${TRELLO_API_KEY:-}" || -z "${TRELLO_TOKEN:-}" ]]; then
  echo "Faltan TRELLO_API_KEY y/o TRELLO_TOKEN (esperado en $ENV_FILE)" >&2
  exit 1
fi

BASE="https://api.trello.com/1"
LISTS=("Backlog" "En curso" "Revisión supervisor" "Bloqueado" "Hecho")

create_board() {
  local name="$1"
  curl -sS -X POST "$BASE/boards" \
    -d "name=$name" \
    -d "defaultLists=false" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN"
}

add_list() {
  local board_id="$1"
  local list_name="$2"
  curl -sS -X POST "$BASE/lists" \
    -d "name=$list_name" \
    -d "idBoard=$board_id" \
    -d "pos=bottom" \
    -d "key=$TRELLO_API_KEY" \
    -d "token=$TRELLO_TOKEN"
}

bootstrap_board() {
  local title="$1"
  echo "Creando tablero: $title" >&2
  local resp
  resp="$(create_board "$title")"
  if echo "$resp" | jq -e .id >/dev/null 2>&1; then
    :
  else
    echo "$resp" >&2
    echo "ERROR: no se pudo crear el tablero (¿token solo lectura? Ver docs/BOOTSTRAP_ESQUELETO_TRELLO_DISCORD.md)" >&2
    exit 1
  fi
  local bid
  bid="$(echo "$resp" | jq -r .id)"
  echo "  id=$bid  url=$(echo "$resp" | jq -r .url)" >&2
  for L in "${LISTS[@]}"; do
    add_list "$bid" "$L" >/dev/null
    echo "  lista: $L" >&2
  done
  echo "$resp"
}

echo "=== Tableros ===" >&2
R1="$(bootstrap_board "Empresa-marketing - Operaciones")"
R2="$(bootstrap_board "Empresa-ventas - Operaciones")"
echo "" >&2
echo "=== Resumen (JSON ids) ===" >&2
echo "$R1" | jq '{name, id, url}'
echo "$R2" | jq '{name, id, url}'
echo "" >&2
echo "Pega los id en agents/jarvis/MEMORY.md (tabla Trello)." >&2
