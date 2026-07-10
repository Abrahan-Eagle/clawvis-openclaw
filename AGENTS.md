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
node agent-town/scripts/check-prod-server-signatures.mjs
```

## graphify

Si existe un grafo local regenerable:

- Antes de preguntas de arquitectura, **si** `graphify-out/GRAPH_REPORT.md` existe, léelo (god nodes / comunidades).
- Si `graphify-out/wiki/index.md` existe, preférelo a archivos crudos.
- Tras modificar código en una sesión: `graphify update .` (AST-only) para mantener el grafo.

`graphify-out/` está en `.gitignore` — no asumas que el archivo está en el clon.
