#!/usr/bin/env bash
# Valida las 40 marketing skills importadas (frontmatter, atribucion, enlaces relativos).
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$DIR/scripts/validate_marketing_skills.py" "$@"
