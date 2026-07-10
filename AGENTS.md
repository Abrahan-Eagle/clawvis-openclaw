# AGENTS.md — clawvis-openclaw

Monorepo operativo: **OpenClaw** (gateway) + **jarvis-ecosystem** + **Agent Town**.

## Antes de cambios no triviales

1. Leer [README.md](README.md) y [docs/INFORME_FORENSE_360_2026-07.md](docs/INFORME_FORENSE_360_2026-07.md) si el trabajo toca seguridad o estado.
2. Política de estado: [docs/OPENCLAW_STATE_GIT_POLICY.md](docs/OPENCLAW_STATE_GIT_POLICY.md).
3. Plantilla sanitizada: [config/openclaw-home/README.md](config/openclaw-home/README.md).
4. Threat model token UI: [agent-town/docs/THREAT_MODEL_GATEWAY_TOKEN.md](agent-town/docs/THREAT_MODEL_GATEWAY_TOKEN.md).

## Verificaciones rápidas

```bash
bash scripts/check-no-secrets.sh
bash jarvis-ecosystem/scripts/sync-automations-yaml.sh --check
cd agent-town && pnpm test
```

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- After modifying code files in this session, run `graphify update .` to keep the graph current (AST-only, no API cost)
