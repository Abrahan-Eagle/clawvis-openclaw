#!/usr/bin/env bash
# Smoke: levanta JMC en puerto aleatorio, curl /v1/*, apaga.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/jmc/adapter"
TOKEN="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
PORT="$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()')"
SMOKE_JSON="$(mktemp)"
export JMC_BEARER_TOKEN="$TOKEN"
export JMC_REPO_ROOT="$ROOT"

UV="${ROOT}/.venv-jmc/bin/uvicorn"
if [[ ! -x "$UV" ]]; then UV="$(command -v uvicorn)"; fi
if [[ ! -x "$UV" ]]; then
  echo "ERROR: no hay uvicorn ejecutable. Crea el venv: cd \"$ROOT\" && python3 -m venv .venv-jmc && .venv-jmc/bin/pip install -e jmc/adapter" >&2
  exit 1
fi
PY="$(dirname "$UV")/python"
if ! (cd "$ROOT/jmc/adapter" && "$PY" -c "import app.main" 2>/dev/null); then
  echo "ERROR: el venv no tiene el adapter JMC (import app.main falló). Ejecuta: cd \"$ROOT\" && .venv-jmc/bin/pip install -e jmc/adapter" >&2
  exit 1
fi

"$UV" app.main:app --host 127.0.0.1 --port "$PORT" &
PID=$!
cleanup() {
  rm -f "$SMOKE_JSON" 2>/dev/null || true
  kill "$PID" 2>/dev/null || true
  wait "$PID" 2>/dev/null || true
}
trap cleanup EXIT

AUTH=(-H "Authorization: Bearer ${TOKEN}")

ready=0
for _ in $(seq 1 50); do
  if curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/health" -o /dev/null; then
    ready=1
    break
  fi
  sleep 0.12
done
if [[ "$ready" != 1 ]]; then
  echo "ERROR: el adapter no respondió a /v1/health a tiempo (puerto ${PORT})." >&2
  exit 1
fi

curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/health" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert d["meta"]["version"]=="v1"; assert d["data"]["status"]=="ok"; assert "brand" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/system/metrics" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); x=d["data"]; assert "cpu_percent" in x and "mem" in x'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/runtime/services" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert isinstance(d["data"]["services"], list)'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/openclaw/cron-timeline?days=7" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); x=d["data"]; assert x.get("window_days")==7 and "agents" in x'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/memory/list" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "items" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/files/tree?root=docs" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert d["data"].get("root")=="docs" and "entries" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/search/?q=Mission" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "hits" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/modes/current" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "effective_mode" in d["data"]; assert d["data"].get("mode_write_enabled") is True'
SMOKE_POST="$(curl -sS -o "$SMOKE_JSON" -w "%{http_code}" -X POST "${AUTH[@]}" -H "Content-Type: application/json" \
  "http://127.0.0.1:${PORT}/v1/modes/current" -d '{"mode":"C"}')"
test "$SMOKE_POST" = "200"
python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); assert d["data"]["effective_mode"]=="C"' "$SMOKE_JSON"
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/modes/matrix" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "matrix" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/state/tasks" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "tasks" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/state/summary" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); x=d["data"]; assert "open_tasks" in x and "pending_approvals" in x and "tag_counts" in x'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/state/tag-stats" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); x=d["data"]; assert "tag_counts" in x and "unique_tags" in x'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/state/activity?limit=50" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "events" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/state/activity?limit=300" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "events" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/openclaw/gateway?window_hours=24" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); x=d["data"]; assert "agents" in x and "totals" in x and x["window_hours"]==24'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/costs/summary" \
  | python3 -c 'import sys,json; json.load(sys.stdin)'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/judge/last" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "runs" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/modes/doc_fragment" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "snippet" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/state/handoffs" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert isinstance(d["data"]["handoffs"], list)'

# --- v1.10 ---
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/health/deep" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "data" in d and "openclaw_json" in d["data"]'
curl -sf "http://127.0.0.1:${PORT}/v1/auth/status" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert d["data"].get("locked") is False or d["data"].get("locked") is True'
curl -sfS -o /dev/null -X POST "http://127.0.0.1:${PORT}/v1/csp-report" -H "Content-Type: application/json" -d '{"csp-report":{}}'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/state/agents-stats" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "top_agents_24h" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/state/zombies?hours=72" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "items" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/state/latency" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "by_agent" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/skills/coverage" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "agents" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/heartbeats/coverage" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "missing_heartbeat" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/diagnostics" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "repo_root" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/docs/lints" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "ok" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/system/cpu-detail" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "per_cpu_percent" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/system/proc-summary" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "processes_scanned" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/system/fs-latency" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "stat_ms" in d["data"] or "error" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/external/healthchecks" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "items" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/runtime/services" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "services" in d["data"]'
curl -sf "${AUTH[@]}" "http://127.0.0.1:${PORT}/v1/webhooks/status" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert "configured" in d["data"]'

echo "jmc-smoke: OK (puerto ${PORT})"
