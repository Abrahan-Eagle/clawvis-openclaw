---
name: model-router
description: Política del router local de modelos (reglas YAML + script CLI); no sustituye bindings de canales.
---

# Model router (Jarvis)

## Qué es

- Archivo de reglas: `model-router.rules.yaml` en este workspace.
- Resolución: `scripts/model-router.mjs` (Node, dependencia `yaml` en `scripts/package.json`).
- **Canales (Telegram, etc.):** OpenClaw **no** aplica este router automáticamente; los hooks `message:*` no mutan el modelo del turno. El router sirve para **CLI**, scripts y automatizaciones.

## Uso rápido (CLI)

```bash
cd scripts && npm install
node model-router.mjs --json "tu mensaje"
./jarvis-agent-routed.sh "tu mensaje"
```

## Agentes esperados

El YAML referencia `jarvis-auto-light`, `jarvis` (estándar), `jarvis-deep`. Deben existir en `agents.list` con `model.primary` acorde. Ver `docs/openclaw.model-router.agents.snippet.json` en el repo clawvis-openclaw.

## Clasificador opcional

Si `JARVIS_MODEL_ROUTER_CLASSIFIER=1` y `GROQ_API_KEY` está en el entorno, mensajes largos sin regla explícita pueden clasificarse con `llama-3.1-8b-instant` (JSON `tier`).

## Variables útiles

| Variable | Efecto |
|----------|--------|
| `JARVIS_MODEL_ROUTER_RULES` | Ruta absoluta al YAML |
| `JARVIS_AGENT_LIGHT` / `STANDARD` / `HEAVY` | Override de `agentId` por tier |
| `JARVIS_ROUTER_VERBOSE=1` | `jarvis-agent-routed.sh` imprime JSON al stderr |
