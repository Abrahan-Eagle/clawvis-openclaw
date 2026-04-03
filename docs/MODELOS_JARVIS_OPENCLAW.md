# Modelos LLM: Jarvis / OpenClaw

Este documento describe la política **ligero vs fuerte**, la diferencia entre **fallbacks** y un **router por tarea**, el **router implementado en el repo** (reglas + CLI), y el consumo en reposo. La configuración viva está en `~/.openclaw/openclaw.json` (no versionar secretos).

### Solo modelos ya en tu OpenClaw

Los tiers del router (`groq/...`, `opencode/...`) deben coincidir con IDs que ya tengas en `agents.defaults.models` (o en el bloque `model` del agente). **No** se añaden proveedores nuevos: el clasificador opcional (Fase 2) usa **la misma API Groq** que ya configuras en auth/OpenClaw (`llama-3.1-8b-instant`), y **por defecto está desactivado** (`JARVIS_MODEL_ROUTER_CLASSIFIER` sin `1` → solo reglas, 0 llamadas extra).

### Checklist operativa (agentes nuevos del router)

Cuando añadas `jarvis-auto-light` y `jarvis-deep` a `agents.list`, OpenClaw usa **un directorio de agente distinto** (`~/.openclaw/agents/<id>/agent/`). Copia las credenciales del Jarvis principal:

```bash
for id in jarvis-auto-light jarvis-deep; do
  mkdir -p "$HOME/.openclaw/agents/$id/agent"
  cp -a "$HOME/.openclaw/agents/jarvis/agent/auth-profiles.json" \
    "$HOME/.openclaw/agents/$id/agent/auth-profiles.json"
done
```

(o equivalente con `openclaw agents add <id>`). Sin esto, verás `No API key found for provider` para ese `agentId`. Si el gateway sigue cacheando estado, reinicia el servicio OpenClaw.

## Fallbacks ≠ “Auto” por tarea

| Mecanismo | Qué hace |
|-----------|----------|
| **`primary` + `fallbacks`** (en `agents.defaults.model` o por agente) | Si el modelo **falla** (401, rate limit, modelo desconocido, etc.), el gateway prueba el siguiente de la lista. **No** cambia de modelo si la respuesta es “mala pero válida”. |
| **Router por tarea** (tipo Cursor Auto) | **No** está integrado en el core de OpenClaw 2026.4.x como hook que cambie el modelo **antes** de cada turno en canales. Los eventos `message:preprocessed` / hooks de workspace son **informativos** (no mutan el pipeline). `openclaw agent` **no** expone `--model`; el modelo viene de `agents.list` + defaults. |

## Fase 0 — Decisión de integración (investigación)

| Opción | Resultado |
|--------|-----------|
| Plugin / hook que fije `modelRef` por mensaje | **No** hay API estable documentada equivalente a “pre-inferencia + override” para mensajes de Telegram/Discord sin modificar el core. |
| **Plan B adoptado** | **Motor declarativo** (`model-router.rules.yaml`) + **script Node** (`jarvis-ecosystem/agents/jarvis/scripts/model-router.mjs`) + **wrapper shell** (`jarvis-agent-routed.sh`) que elige **`--agent`** según tier. Los canales siguen usando bindings; para “auto” en chat hace falta otro proceso (bot intermedio) o bindings por peer. |
| Clasificador ligero (opcional) | Implementado: si `JARVIS_MODEL_ROUTER_CLASSIFIER=1` y `GROQ_API_KEY`, mensajes largos sin regla pueden clasificarse vía Groq JSON (`tier`). |

## Router implementado (repo clawvis-openclaw)

| Artefacto | Ruta |
|-----------|------|
| Reglas (prioridad = orden, primera coincidencia) | [`jarvis-ecosystem/agents/jarvis/model-router.rules.yaml`](../jarvis-ecosystem/agents/jarvis/model-router.rules.yaml) |
| Resolución + JSON | [`jarvis-ecosystem/agents/jarvis/scripts/model-router.mjs`](../jarvis-ecosystem/agents/jarvis/scripts/model-router.mjs) |
| CLI enrutado | [`jarvis-ecosystem/agents/jarvis/scripts/jarvis-agent-routed.sh`](../jarvis-ecosystem/agents/jarvis/scripts/jarvis-agent-routed.sh) |
| Tests de regresión | `node jarvis-ecosystem/agents/jarvis/scripts/test-model-router.mjs` (tras `npm install` en `scripts/`) |
| Skill | [`jarvis-ecosystem/agents/jarvis/skills/model-router/SKILL.md`](../jarvis-ecosystem/agents/jarvis/skills/model-router/SKILL.md) |
| Fragmento `agents.list` | [`docs/openclaw.model-router.agents.snippet.json`](openclaw.model-router.agents.snippet.json) |

### Tiers por defecto (catálogo actual)

| Tier | Modelo canónico | Agente sugerido (`--agent`) |
|------|------------------|-----------------------------|
| Ligero | `groq/llama-3.1-8b-instant` | `jarvis-auto-light` |
| Estándar | `groq/llama-3.3-70b-versatile` | `jarvis` |
| Fuerte | `opencode/nemotron-3-super-free` | `jarvis-deep` |

Debes definir **`jarvis-auto-light`** (y opcionalmente ajustar `jarvis` / `jarvis-deep`) en `~/.openclaw/openclaw.json` con el mismo `workspace` que Jarvis y `model.primary` acorde. Usa el fragmento JSON de referencia y fusiona manualmente.

### Uso local (CLI)

```bash
cd jarvis-ecosystem/agents/jarvis/scripts
npm install
node model-router.mjs --json "hola"
node model-router.mjs --json "debug segfault en production"
./jarvis-agent-routed.sh "tu mensaje"   # ejecuta openclaw agent con el agente resuelto
```

Variables útiles: `JARVIS_MODEL_ROUTER_RULES`, `JARVIS_AGENT_LIGHT`, `JARVIS_AGENT_STANDARD`, `JARVIS_AGENT_HEAVY`, `JARVIS_ROUTER_VERBOSE=1`, `JARVIS_MODEL_ROUTER_CLASSIFIER=1`, `GROQ_API_KEY`.

### Nota sobre regex

Las reglas usan sintaxis tipo PCRE con `(?i)`; el script traduce `(?i)` a flag `i` de JavaScript. Los patrones se prueban con `RegExp` (flag `s` para `.` multilínea).

## Política recomendada (config global)

- **`agents.defaults.model`:** `primary` + `fallbacks` solo ante **error** de proveedor.
- **Canales:** bindings por defecto → `jarvis`; modo fuerte con agente dedicado (`jarvis-deep`) vía binding específico o CLI.

## Cómo usar el modo profundo (sin router)

1. **CLI:**

   ```bash
   openclaw agent --agent jarvis-deep --message "Tu pregunta compleja"
   ```

2. **Canales:** Añade un `binding` **más específico** que el `*` y colócalo **antes** en la lista. Ver [docs.openclaw.ai](https://docs.openclaw.ai).

## Consumo en reposo

| Componente | Idle |
|------------|------|
| Gateway OpenClaw | Proceso activo, poco CPU; **no** llama a LLMs solo por estar encendido. |
| APIs (Groq, OpenCode, OpenRouter) | Sin requests → sin coste por tokens. |
| Clasificador opcional | Solo si activas env + mensaje largo sin regla; 1 request extra a Groq. |
| Ollama | Sin servicio o sin modelo cargado → sin inferencia local. |

## Matriz de pruebas (router)

| Mensaje de prueba | Tier esperado (reglas actuales) |
|-------------------|---------------------------------|
| `hola` | light (trivial) |
| `qué tiempo hace en Madrid` | light (trivial / clima) |
| `debug this NullPointerException` | standard (código) |
| `refactor the whole distributed system` | heavy |
| `short` (≤40 chars, sin otras reglas) | light (corto) |
| 600× `x` sin palabras clave | light por defecto; con `JARVIS_MODEL_ROUTER_CLASSIFIER=1` puede variar |

Validación automatizada: `node scripts/test-model-router.mjs`. Validación instalación: `openclaw doctor` (exit 0; warnings habituales según entorno).

## Matriz orientativa (operación)

| Situación | Agente / modelo |
|-----------|------------------|
| Uso diario, canales | `jarvis` (según tu `primary`) |
| Razonamiento largo, prioridad calidad | `jarvis-deep` o CLI |
| Router CLI / scripts | `jarvis-agent-routed.sh` + reglas YAML |
| Privacidad / offline | Ollama en local |

## Fragmento de referencia (`agents.list`)

Ejemplo alineado al router (ajusta `workspace`):

```json
{
  "id": "jarvis",
  "default": true,
  "workspace": "/home/aipp/jarvis-ecosystem/agents/jarvis"
},
{
  "id": "jarvis-auto-light",
  "workspace": "/home/aipp/jarvis-ecosystem/agents/jarvis",
  "model": {
    "primary": "groq/llama-3.1-8b-instant",
    "fallbacks": ["groq/llama-3.3-70b-versatile", "opencode/nemotron-3-super-free"]
  }
},
{
  "id": "jarvis-deep",
  "workspace": "/home/aipp/jarvis-ecosystem/agents/jarvis",
  "model": {
    "primary": "opencode/nemotron-3-super-free",
    "fallbacks": ["opencode/mimo-v2-pro-free", "groq/llama-3.3-70b-versatile"]
  }
}
```

Ajusta rutas `workspace` si tu usuario no es `aipp`.

## Límites vs Cursor “Auto”

- **Cursor** puede enrutar por turno dentro del IDE; **aquí** el router **solo** aplica donde ejecutes el script (CLI/automatización), salvo que montes otra capa frente a los canales.
- **Sin doble latencia** en la ruta por defecto (solo reglas). El clasificador añade ~1 llamada Groq cuando está activo y se cumplen las condiciones.

## Operación y forense (sesiones, LLM, secretos)

Para baseline (`openclaw doctor`, correlación con logs), integridad de `sessions.json` ↔ `.jsonl`, mínimo `contextTokens` (≥16000), rotación de tokens y checklist de rutas legadas (`/home/will` en archivos viejos), ver el runbook:

- [`docs/OPENCLAW_FORENSE_RUNBOOK.md`](OPENCLAW_FORENSE_RUNBOOK.md)

Script opcional: `jarvis-ecosystem/agents/jarvis/scripts/validate-jarvis-sessions.mjs`.

## Cierre de módulo — Ollama local (abril 2026)

En el host de referencia se **cerró** el módulo de instalación y operación de **Ollama** como proveedor local del Gateway (modelos acotados a ~4GB VRAM, servicio `systemd --user`, enlaces en `~/.openclaw/openclaw.json`, verificación de canales). Detalle operativo, rutas, checklist y límites (`contextTokens` ≥ 16000):

- [`docs/CIERRE_MODULO_OLLAMA_LOCAL.md`](CIERRE_MODULO_OLLAMA_LOCAL.md)
