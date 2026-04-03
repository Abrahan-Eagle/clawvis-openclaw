#!/usr/bin/env bash
# lead-qualifier no tiene metadata.json en el registry remoto; clawflows check no aplica.
# Esta automatizacion requiere curl y jq en PATH (ver automations/registry/lead-qualifier.yaml).

set -euo pipefail
ok=1
for cmd in curl jq; do
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "OK: $cmd -> $(command -v "$cmd")"
  else
    echo "FALTA: $cmd (apt install curl jq o equivalente)" >&2
    ok=0
  fi
done
[[ "$ok" -eq 1 ]] && echo "Requisitos locales de lead-qualifier satisfechos."
