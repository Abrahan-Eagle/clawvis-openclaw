#!/usr/bin/env bash
# Smoke maestro: activity-log tags + JMC adapter (sin nuevas dependencias).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== jarvis-ecosystem-smoke: activity-log tags =="
bash "$ROOT/scripts/activity-log-tags-smoke.sh"

echo "== jarvis-ecosystem-smoke: JMC adapter =="
bash "$ROOT/scripts/jmc-smoke.sh"

echo "jarvis-ecosystem-smoke: OK"
