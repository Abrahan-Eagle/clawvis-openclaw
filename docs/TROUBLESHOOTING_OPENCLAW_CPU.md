# OpenClaw / Jarvis: CPU al 100% y proceso `rg` (ripgrep)

## Síntoma

- El sistema se vuelve lento o inusable; en `top` aparece **`rg`** (ripgrep) con **muchos núcleos al 100%** (p. ej. `%CPU` > 100%).
- El bot (Telegram, Discord, etc.) **no responde** a tiempo o se queda sin mensaje tras una pregunta del usuario.

Eso **no** es “el LLM pensando”: es **búsqueda de texto masiva en disco**, típica de herramientas de búsqueda en workspace que el agente invoca (o efectos encadenados).

## Verificación rápida en el host

```bash
du -sh ~/.openclaw/workspace
du -sh ~/.openclaw
```

En un equipo de referencia (abr 2026) `~/.openclaw/workspace` midió ~8 MiB y `~/.openclaw` ~114 MiB; aun así un `rg` amplio sobre **otras rutas** (p. ej. monorepo vía herramientas) puede saturar CPU. Si el workspace crece (clones, `node_modules`), el riesgo aumenta.

Opcional: localizar `node_modules` bajo el workspace:

```bash
find ~/.openclaw/workspace -maxdepth 4 -type d -name node_modules 2>/dev/null
```

## Tres fuentes típicas de spike (análisis abr 2026)

| Fuente | Qué ves | Mitigación |
|--------|---------|------------|
| **1. Cursor Agent `rg`** | `ps` muestra `.../cursor-agent/.../rg` al ~100% CPU | [`.cursorignore`](../.cursorignore), [`.rgignore`](../.rgignore) (ripgrep nativo), [`.vscode/settings.json`](../.vscode/settings.json), *Reload Window* en Cursor. Monorepo ~1.3 GiB (`agent-town/node_modules` + `.next`). |
| **2. Gateway / `memorySearch` + Ollama** | `openclaw-gateway` u **`ollama`** suben en cada turno o al reiniciar | `sync.watch: false`, `sync.onSessionStart: false`, **`sync.onSearch: false`** (ver trampa abajo). Embeddings híbridos (`query.hybrid`) también cargan CPU en cada búsqueda de memoria. |
| **3. Heartbeats de agentes** | Picos periódicos si hay muchos agentes con heartbeat | Quitar `heartbeat` de agentes aún no operativos (p. ej. `mkt-content`, `sales-hunter`); el `jarvis` principal puede mantener el suyo. |

Coincidencia habitual: preguntar “qué LLM usas” **no** dispara solo la inferencia; a menudo coincide con **indexación del IDE** o con **lectura/búsqueda** en el workspace.

### Trampa: `sync.onSearch: true` y “cualquier pregunta”

Si **`onSearch` está en `true`**, OpenClaw puede **sincronizar el índice de memoria cada vez que se ejecuta una búsqueda en memoria** — y en conversación eso suele ocurrir **en muchos mensajes seguidos**. Eso dispara **embeddings locales (Ollama / `nomic-embed-text`)** y parece que “cualquier cosa que le preguntes a Jarvis” satura el CPU, aunque no sea `rg`.

**Mitigación estable (host sensible):** `onSearch: false`, `onSessionStart: false`, `watch: false`. El índice queda menos “fresco” en caliente; si necesitas reindexar, hazlo con comandos/manuales puntuales o sube recursos.

## Auditoría git (desde `8eb55a53`, abr 2026)

Entre ese commit y `HEAD` entraron **muchas** extensiones a `jarvis-ecosystem/` (skills forenses, Graphify, last30days, docs de gobierno, tablas de skills). Eso **no es un bug por sí solo**, pero:

- **`AGENTS.md` creció** con protocolos “obligatorios” y lecturas de arranque — el modelo puede **intentar más herramientas o lecturas** por turno.
- **MCP** (MemPalace, Graphify) añade superficie: úsalo con criterio; no todo mensaje debería invocarlos.

Si el cuello es **`rg`**, sigue siendo prioridad **Cursor + `.cursorignore` / `.rgignore`**. Si el cuello es **`ollama` o `openclaw-gateway`**, prioriza **`memorySearch.sync`** y carga de embeddings como arriba.

## Causas probables (detalle)

1. El modelo intenta responder “qué modelo uso” **buscando** cadenas (`model`, `primary`, etc.) en lugar de leer **un único** `openclaw.json` acotado o usar metadata de sesión.
2. **Varias herramientas en paralelo** (`maxConcurrent`, subagentes) multiplican búsquedas.
3. **`memorySearch`** con sincronización agresiva (`sync.onSearch` en cada búsqueda, `watch`, `onSessionStart`) añade trabajo de indexación (Ollama + embeddings); suele mostrarse como `ollama` u otro proceso, pero puede coincidir en el tiempo con búsquedas.

### Ripgrep de Cursor Agent (muy frecuente en monorepos)

Si en `ps aux` el comando es **`.../cursor-agent/.../rg --files`** con muchos `--iglob`, es el **indexado del IDE Cursor**, no OpenClaw. En este repo `agent-town/` puede superar **1 GiB** (`node_modules` + `.next`); aunque `rg` excluya `node_modules` en la línea de comandos, el recorrido del disco puede seguir siendo caro.

**Diagnóstico en 5 s:**

```bash
ps aux | grep -E 'cursor-agent.*rg|openclaw'
```

- Si ves **`cursor-agent`** → el pico **no** lo arregla `openclaw.json`; mitiga con **`.cursorignore`**, [`.vscode/settings.json`](../.vscode/settings.json) (`search.exclude` / `files.watcherExclude`), cerrar Cursor, o abrir solo subcarpetas pequeñas.
- Si solo **`openclaw-gateway`** → revisa memoria concurrente y herramientas (secciones de abajo).

**Qué hacer (Cursor):** la raíz del repo incluye [`.cursorignore`](../.cursorignore) y [`.rgignore`](../.rgignore) (mismas rutas; `rg` respeta `.rgignore` aunque otra herramienta ignore exclusiones). Tras cambiarlos, **recarga la ventana** de Cursor (`Developer: Reload Window`) para que el indexador vuelva a leer exclusiones.

Los ítems 1–3 de la lista anterior se refieren al **agente OpenClaw**; si el `rg` es de Cursor, **`openclaw.json` solo no basta**.

## Mitigación en configuración (fuente de verdad: `~/.openclaw/openclaw.json`)

Tras editar, reiniciar el gateway, p. ej.:

`systemctl --user restart openclaw-gateway`

Valores **conservadores** alineados al snapshot sanitizado en el repo ([`config/openclaw-home/openclaw.json`](../config/openclaw-home/openclaw.json)):

| Clave | Objetivo |
|-------|----------|
| `agents.defaults.memorySearch.sync.watch` | `false` — sin file watchers permanentes sobre workspaces (menos re-indexaciones). |
| `agents.defaults.memorySearch.sync.onSessionStart` | `false` — no indexar al abrir cada sesión. |
| `agents.defaults.memorySearch.sync.onSearch` | `false` — evita sincronizar el índice en **cada** búsqueda de memoria (si está `true`, puede disparar CPU en casi cada mensaje). |
| `agents.defaults.maxConcurrent` | `2` — menos llamadas a herramientas en paralelo. |
| `agents.defaults.subagents.maxConcurrent` | `4` — menos subagentes concurrentes. |

**Obligatorio:** los valores anteriores deben existir en **`~/.openclaw/openclaw.json`** (no solo en Git). Tras editar: `systemctl --user restart openclaw-gateway`.

## Higiene del workspace

- No uses `~/.openclaw/workspace` como depósito de monorepos gigantes sin necesidad.
- Mantén `.gitignore` efectivo donde aplique para que herramientas no indexen basura innecesaria.

## Guardrails de comportamiento (prompt)

En [`jarvis-ecosystem/agents/jarvis/AGENTS.md`](../jarvis-ecosystem/agents/jarvis/AGENTS.md) hay reglas: para “qué LLM” **no** búsquedas masivas; lectura acotada de `openclaw.json` o metadata.

## Herramientas `exec` y perfiles (`tools`)

**`exec`** en `tools.alsoAllow` permite comandos shell; sube el riesgo de `rg` u otros escaneos. El snapshot en repo (**[`config/openclaw-home/openclaw.json`](../config/openclaw-home/openclaw.json)**) deja solo `lobster` y `browser` en `alsoAllow` (sin `exec`) para canales de mensajería salvo que vuelvas a añadirlo a mano.

**Criterio:** si necesitas `exec` para automatizaciones concretas, añádelo de nuevo en `~/.openclaw/openclaw.json` y reinicia el gateway; asume el trade-off.

## Si el sistema ya está colgado

1. Identificar PID: `top` o `pgrep -a rg`.
2. Si es seguro: `kill <PID>` del `rg` runaway (o `killall rg` con cuidado).
3. Reiniciar el gateway si el proceso del agente quedó inconsistente.

## Referencias

- [MODELOS_JARVIS_OPENCLAW.md](./MODELOS_JARVIS_OPENCLAW.md) — política de modelos y dónde se define.
- [SECURITY_GATEWAY.md](../jarvis-ecosystem/docs/SECURITY_GATEWAY.md) — gateway y superficie de red.
- [COHERENCIA_RUNTIME_REPO.md](../jarvis-ecosystem/docs/COHERENCIA_RUNTIME_REPO.md) — snapshot vs `~/.openclaw`.
