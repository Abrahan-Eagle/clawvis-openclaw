#!/usr/bin/env bash
# Diagnostico read-only: conectividad hacia el endpoint MCP de Composio (sin credenciales de sesion MCP completas).
# No sustituye `openclaw composio doctor` ni el gateway en runtime.
# Ver: jarvis-ecosystem/docs/TROUBLESHOOTING_COMPOSIO_OPENCLAW.md

set -euo pipefail

MCP_URL="${COMPOSIO_MCP_URL:-https://connect.composio.dev/mcp}"

echo "=== Composio MCP diagnose (read-only) ==="
echo "URL: $MCP_URL"
echo

if command -v curl >/dev/null 2>&1; then
  echo "--- curl -I (headers) ---"
  curl -sS -I --connect-timeout 10 "$MCP_URL" | head -20 || echo "curl failed"
  echo
fi

if command -v node >/dev/null 2>&1; then
  echo "--- node fetch (status code) ---"
  node -e "fetch('$MCP_URL').then(r=>console.log('HTTP',r.status)).catch(e=>console.error('ERR',e.cause||e.message))"
  echo
fi

echo "=== Fin ==="
echo "Un GET anonimo suele devolver 401; eso indica TLS/DNS OK."
echo "Si el gateway falla pero esto pasa, revisar proxy, NODE_USE_ENV_PROXY y plugin @composio/openclaw-plugin."
