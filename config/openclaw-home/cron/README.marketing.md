# Cron OpenClaw — marketing loop (plantilla)

Los jobs **no** se activan solos. Copia entradas de [`jobs.marketing-orchestrator.example.json`](jobs.marketing-orchestrator.example.json) a `~/.openclaw/cron/jobs.json` solo con OK explícito del CEO, luego reinicia el gateway.

## Jobs incluidos (disabled por defecto en el ejemplo)

| id | agentId | Cadencia | Qué hace |
|----|---------|----------|----------|
| `jarvis-marketing-orchestrator` | jarvis | cada 3h | Corre dispatcher + revisa handoffs; no publica |
| `mkt-content-due-calendar` | mkt-content | L–V 09:00 | `editorial-calendar due` → una unidad de producción |

## Relacionado

- Heartbeats en plantilla: [`jarvis-ecosystem/openclaw.json`](../../jarvis-ecosystem/openclaw.json)
- Dispatcher: [`jarvis-ecosystem/scripts/marketing-dispatch.sh`](../../jarvis-ecosystem/scripts/marketing-dispatch.sh)
- Runtime: fusionar heartbeats a `~/.openclaw/openclaw.json` (ver `docs/JMC_OPERACION.md` y `docs/HEARTBEAT_OPERATIVO.md`)
