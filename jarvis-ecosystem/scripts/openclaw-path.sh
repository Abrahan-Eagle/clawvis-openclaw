#!/usr/bin/env bash
# Expone en PATH el bin de Node (nvm) donde suele instalarse el CLI `openclaw`, para
# shells no interactivos, CI o agentes que no cargan ~/.bashrc.
# Uso (desde jarvis-ecosystem):  source scripts/openclaw-path.sh
# Opcional: OPENCLAW_NODE_VERSION=22  (o "20", "lts/*", etc. — lo que acepta nvm use)

# Debe ser sourceado (no ejecutado) para afectar al shell del caller.
if [ "${BASH_SOURCE[0]}" -ef "$0" ] 2>/dev/null || [ -z "${BASH_SOURCE[0]:-}" ]; then
  echo "Uso: source ${BASH_SOURCE[0]:-$0}" >&2
  echo "O desde jarvis-ecosystem:  . scripts/openclaw-path.sh" >&2
  exit 1
fi

if command -v openclaw >/dev/null 2>&1; then
  return 0 2>/dev/null || :
fi

NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
if [ -s "$NVM_DIR/nvm.sh" ]; then
  # shellcheck disable=SC1090
  . "$NVM_DIR/nvm.sh"
  if [ -n "${OPENCLAW_NODE_VERSION:-}" ]; then
    nvm use "$OPENCLAW_NODE_VERSION" --silent 2>/dev/null || true
  else
    nvm use default --silent 2>/dev/null || nvm use 22 --silent 2>/dev/null || nvm use 20 --silent 2>/dev/null || nvm use node --silent 2>/dev/null || true
  fi
fi

if ! command -v openclaw >/dev/null 2>&1; then
  for d in "$HOME"/.nvm/versions/node/v*/bin; do
    [ -d "$d" ] || continue
    if [ -e "$d/openclaw" ]; then
      case ":$PATH:" in
        *":$d:"*) ;;
        *) export PATH="$d:$PATH" ;;
      esac
      break
    fi
  done
fi

if ! command -v openclaw >/dev/null 2>&1; then
  echo "openclaw-path.sh: 'openclaw' sigue sin estar en PATH. Instala: npm i -g openclaw (con el Node que uses) o ajusta OPENCLAW_NODE_VERSION." >&2
  return 1 2>/dev/null || true
fi

return 0 2>/dev/null || true
