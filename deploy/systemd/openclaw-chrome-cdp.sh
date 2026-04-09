#!/usr/bin/env bash
# Chrome persistente con CDP en 127.0.0.1:18800 para OpenClaw (perfil openclaw, attachOnly).
set -euo pipefail
exec /usr/bin/google-chrome \
  --headless=new \
  --no-sandbox \
  --disable-gpu \
  --disable-dev-shm-usage \
  --remote-debugging-port=18800 \
  --remote-debugging-address=127.0.0.1 \
  --remote-allow-origins=* \
  --user-data-dir="${HOME}/.openclaw/browser/openclaw/user-data" \
  about:blank
