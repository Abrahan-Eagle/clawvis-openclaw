#!/usr/bin/env bash
# DEPRECADO (JMC v1.8+): POST /v1/modes/current ya no depende de JMC_ALLOW_MODE_WRITE.
# Solo hace falta un Bearer válido (JMC_BEARER_TOKEN). Este script no modifica ficheros ni systemd.
set -euo pipefail

echo "Este script está deprecado."
echo "JMC v1.8+ permite POST /v1/modes/current con Authorization: Bearer válido."
echo "La variable JMC_ALLOW_MODE_WRITE se ignora si aún aparece en vuestro .env."
exit 0
