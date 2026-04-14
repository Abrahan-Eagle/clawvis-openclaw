#!/usr/bin/env bash
set -euo pipefail

# Reporte de uso/costes por agente - parsea sesiones JSONL de OpenClaw
# Uso: ./scripts/cost-report.sh [YYYY-MM]
# Sin argumento: mes actual.

OPENCLAW_DIR="${OPENCLAW_HOME:-$HOME/.openclaw}"
AGENTS_DIR="$OPENCLAW_DIR/agents"
MONTH="${1:-$(date +%Y-%m)}"

if [ ! -d "$AGENTS_DIR" ]; then
  echo "ERROR: No se encuentra $AGENTS_DIR"
  exit 1
fi

echo "======================================"
echo " REPORTE DE USO — $MONTH"
echo " Directorio: $AGENTS_DIR"
echo " Generado: $(date '+%Y-%m-%d %H:%M:%S')"
echo "======================================"
echo ""

python3 - "$AGENTS_DIR" "$MONTH" <<'PYEOF'
import sys, os, json, glob
from collections import defaultdict
from datetime import datetime

agents_dir = sys.argv[1]
target_month = sys.argv[2]

report = {}

for agent_name in sorted(os.listdir(agents_dir)):
    sessions_dir = os.path.join(agents_dir, agent_name, "sessions")
    if not os.path.isdir(sessions_dir):
        continue

    stats = {
        "sessions": 0,
        "messages_user": 0,
        "messages_assistant": 0,
        "chars_user": 0,
        "chars_assistant": 0,
        "models_used": defaultdict(int),
        "first_ts": None,
        "last_ts": None,
    }

    for f in glob.glob(os.path.join(sessions_dir, "*.jsonl")):
        session_in_month = False
        current_model = "unknown"

        try:
            with open(f) as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        ev = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    ts = ev.get("timestamp", "")
                    if isinstance(ts, str) and ts[:7] == target_month:
                        session_in_month = True
                    elif isinstance(ts, (int, float)):
                        dt = datetime.utcfromtimestamp(ts / 1000 if ts > 1e12 else ts)
                        if dt.strftime("%Y-%m") == target_month:
                            session_in_month = True

                    if ev.get("type") == "model_change":
                        mid = ev.get("modelId", "unknown")
                        prov = ev.get("provider", "")
                        current_model = f"{prov}/{mid}" if prov else mid

                    if ev.get("type") == "message" and session_in_month:
                        msg = ev.get("message", {})
                        role = msg.get("role", "")
                        content = msg.get("content", "")
                        if isinstance(content, list):
                            content = " ".join(
                                c.get("text", "") for c in content if isinstance(c, dict)
                            )
                        clen = len(str(content))

                        if role == "user":
                            stats["messages_user"] += 1
                            stats["chars_user"] += clen
                        elif role == "assistant":
                            stats["messages_assistant"] += 1
                            stats["chars_assistant"] += clen
                            stats["models_used"][current_model] += 1

                        ts_val = ts
                        if isinstance(ts_val, str):
                            pass
                        if stats["first_ts"] is None or str(ts_val) < str(stats["first_ts"]):
                            stats["first_ts"] = ts_val
                        if stats["last_ts"] is None or str(ts_val) > str(stats["last_ts"]):
                            stats["last_ts"] = ts_val

        except Exception as e:
            print(f"  WARN: Error leyendo {f}: {e}", file=sys.stderr)
            continue

        if session_in_month:
            stats["sessions"] += 1

    if stats["sessions"] > 0:
        report[agent_name] = stats

if not report:
    print(f"Sin actividad para {target_month}.")
    sys.exit(0)

total_user = 0
total_asst = 0
total_tokens_est = 0

for agent, s in sorted(report.items()):
    tokens_in = s["chars_user"] // 4
    tokens_out = s["chars_assistant"] // 4
    tokens_total = tokens_in + tokens_out
    total_user += tokens_in
    total_asst += tokens_out
    total_tokens_est += tokens_total

    print(f"--- {agent} ---")
    print(f"  Sesiones activas:    {s['sessions']}")
    print(f"  Mensajes (user):     {s['messages_user']}")
    print(f"  Mensajes (assistant):{s['messages_assistant']}")
    print(f"  Tokens est. IN:      {tokens_in:,}")
    print(f"  Tokens est. OUT:     {tokens_out:,}")
    print(f"  Tokens est. TOTAL:   {tokens_total:,}")

    if s["models_used"]:
        top3 = sorted(s["models_used"].items(), key=lambda x: -x[1])[:3]
        models_str = ", ".join(f"{m}({c})" for m, c in top3)
        print(f"  Modelos top:         {models_str}")
    print()

print("======================================")
print(f"  TOTAL tokens est.:   {total_tokens_est:,}")
print(f"    IN  (user):        {total_user:,}")
print(f"    OUT (assistant):   {total_asst:,}")
print(f"  Agentes activos:     {len(report)}")

cost_note = """
  NOTA: Los modelos cursor-local y ollama tienen coste $0.
  Para modelos de pago (groq, openrouter, google), calcular
  con las tarifas vigentes del proveedor.
"""
print(cost_note)
PYEOF
