#!/usr/bin/env bash
# Smoke: activity-log --tags en start + subcomando tag (add/remove/set).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BIN="$ROOT/skills/global/activity-log/bin/activity-log"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

export JARVIS_STATE_DIR="$TMP"
mkdir -p "$TMP/tasks" "$TMP/handoffs" "$TMP/cache/images"
: >"$TMP/activity-log.jsonl"

run_al() {
  env JARVIS_STATE_DIR="$TMP" bash "$BIN" "$@"
}

assert_jq() {
  local file="$1"
  shift
  jq -e "$@" "$file" >/dev/null || {
    echo "ASSERT failed: $file" >&2
    jq . "$file" >&2
    exit 1
  }
}

OUT=$(run_al start --agent jarvis --title "tags smoke" --tags 'urgent, infra')
TASK_ID=$(echo "$OUT" | jq -r .task_id)
[ -n "$TASK_ID" ] && [ "$TASK_ID" != null ]

TF="$TMP/tasks/$TASK_ID.json"
assert_jq "$TF" '.tags == ["urgent","infra"]'

run_al tag "$TASK_ID" --add 'review'
assert_jq "$TF" '.tags | sort == ["infra","review","urgent"]'

run_al tag "$TASK_ID" --remove 'urgent'
assert_jq "$TF" '.tags | sort == ["infra","review"]'

run_al tag "$TASK_ID" --set 'foo'
assert_jq "$TF" '.tags == ["foo"]'

LAST=$(tail -n1 "$TMP/activity-log.jsonl")
echo "$LAST" | jq -e '.type == "tag" and .payload.action == "set"' >/dev/null

echo "activity-log-tags-smoke: OK (task=$TASK_ID)"
