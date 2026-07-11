# Manual RRSS Jarvis — loop de agencia (modo C)

Guía operativa para la empresa de marketing del holding.  
**Modo recomendado:** C — produce assets y handoffs solo; **publica solo con AG-12/13** (CEO).

## Piezas del motor

| Pieza | Ruta | Rol |
|-------|------|-----|
| Heartbeats `mkt-*` | `openclaw.json` (plantilla) | Despierta agentes cada 2h |
| Checklist por rol | `agents/marketing/HEARTBEAT.md` | Qué hacer en cada pulso |
| Dispatcher | `scripts/marketing-dispatch.sh` | Handoffs abiertos → `agentTurn` / system event |
| Cron ejemplo | `config/openclaw-home/cron/jobs.marketing-orchestrator.example.json` | Orquestador jarvis (disabled hasta OK CEO) |

**Runtime:** fusionar heartbeats a `~/.openclaw/openclaw.json` y jobs a `~/.openclaw/cron/jobs.json` solo con tu OK. Reiniciar gateway.

## Skills P0/P1 ejecutables

```bash
cd jarvis-ecosystem
export PATH="$PWD/skills/global/editorial-calendar/bin:$PWD/skills/global/approval-gate/bin:$PWD/skills/global/judge-run/bin:$PWD/skills/global/memory-store/bin:$PWD/skills/global/client-onboard/bin:$PWD/skills/global/mkt-publish/bin:$PWD/skills/global/publish-safety/bin:$PWD/skills/global/creative-qa/bin:$PWD/skills/global/de-ai-ify/bin:$PWD/skills/global/competitor-intel/bin:$PWD/skills/global/social-metrics/bin:$PWD/skills/global/client-report/bin:$PWD/skills/global/handoff/bin:$PWD/skills/global/activity-log/bin:$PATH"
```

| Skill | Comandos clave |
|-------|----------------|
| `client-onboard` | `init`, `brand`, `checklist` |
| `editorial-calendar` | `add`, `list`, `due`, `approve` |
| `competitor-intel` | `ingest`, `viral-analyze --dry-run` |
| `creative-qa` | `check --file`, `batch --dir` |
| `de-ai-ify` | `clean --text` / `--file` |
| `approval-gate` | `request`, `approve`, `check`, `list` |
| `judge-run` | `--handoff …` → `state/judge/judge-*.json` (pre-AG-12) |
| `publish-safety` | `check --account`, `record` |
| `mkt-publish` | `--handoff … --dry-run` (live: Meta + gate) |
| `social-metrics` | `pull --dry-run`, `show` |
| `client-report` | `generate --dossier --period` |
| `executor` | `--live` plan JSON allowlisted |
| `session-compact-ops` | protocolo (sin bin): compactar en fin de fase / pre-gate |
| `memory-store` | `format-prompt` en Session Startup |

## Memoria y aprendizaje (HITL)

```bash
memory-store --file agents/marketing/memory.json format-prompt
bash scripts/memory-consolidate.sh --agent marketing    # propone; --apply solo con OK
bash scripts/lessons-scan.sh                            # candidatos LESSONS.md
```

Context packs: `contexts/research.md` | `produce.md` | `review.md` (`JARVIS_CONTEXT_MODE`).

## Flujo mínimo E2E (dry-run)

1. `client-onboard checklist --dossier corralx`
2. `editorial-calendar due --hours 72 --dossier corralx`
3. Producir asset (`carousel-render` / pipeline existente)
4. `creative-qa check --file <png>` + `de-ai-ify clean …`
5. `handoff create … --schema producer-to-publisher`
6. **`judge-run --handoff … --category carousel_ig`** (revisar score/verdict)
7. `approval-gate request --ag AG-12 --task … --handoff …`
8. CEO: `approval-gate approve --id esc-…`
9. `publish-safety check --account corralx`
10. `mkt-publish --handoff … --dry-run`
11. `editorial-calendar approve --id slot-…` + `client-report generate`

## Stubs `planned`

Skills en `skills/global/` con `status: planned` (sin CLI): no invocar.  
Ej.: `social-concierge`, `viral-trends`, `funnel-metrics`, `lead-capture`, …

## Credenciales Meta (solo env / HOME)

`META_ACCESS_TOKEN`, `META_IG_USER_ID`, `META_ASSET_PUBLIC_URL` — nunca en git.

## Docs relacionados

- [APPROVAL_GATES.md](APPROVAL_GATES.md)
- [AUTONOMIA_MODOS.md](AUTONOMIA_MODOS.md)
- [COORDINACION_AGENTES.md](COORDINACION_AGENTES.md)
- [HEARTBEAT_OPERATIVO.md](HEARTBEAT_OPERATIVO.md)
- [client-dossiers/templates/PROMPTS_RRSS.md](../client-dossiers/templates/PROMPTS_RRSS.md)
