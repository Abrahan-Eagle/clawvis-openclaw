# Proveedor LLM vía Cursor + OpenClaw (comunidad)

**Ámbito:** integración **no oficial** entre la suscripción **Cursor** (Pro/Business) y **OpenClaw**. Cursor no expone una API HTTP pública de “suscripción”; la comunidad envuelve el **Cursor Agent CLI** (`agent` / `cursor-agent`) y expone un endpoint **compatible con OpenAI** en localhost.

**Última revisión documental:** abril 2026.

---

## Aviso legal y de producto

- Revisa los **Términos de servicio de Cursor** respecto al uso del CLI, automatización y proxies. El tráfico de inferencia **sigue yendo a la infraestructura de Cursor** (no es offline).
- Estas herramientas son **terceros** (MIT u otras licencias). No sustituyen soporte oficial de Cursor ni de OpenClaw.
- Mantén **`contextTokens` ≥ 16000** en OpenClaw donde tu versión lo exija (fallos si el valor es menor).

---

## Dos líneas principales

### A) `cursor-agent-api-proxy` (npm, mínimo acoplamiento)

| Recurso | Enlace |
|--------|--------|
| Repositorio | [github.com/tageecc/cursor-agent-api-proxy](https://github.com/tageecc/cursor-agent-api-proxy) |
| Paquete npm | [npmjs.com/package/cursor-agent-api-proxy](https://www.npmjs.com/package/cursor-agent-api-proxy) |
| CLI | `cursor-agent-api` (puerto por defecto **4646**, base `http://localhost:4646/v1`) |

**Flujo:** OpenClaw (u otro cliente OpenAI) → HTTP local → proxy → **spawn** del CLI `agent` → Cursor (nube).

**Requisitos típicos:** Node 20+, CLI Cursor instalado, `agent login` o variable `CURSOR_API_KEY` (clave en [cursor.com/settings](https://cursor.com/settings)).

**Endpoints:** `GET /health`, `GET /v1/models`, `POST /v1/chat/completions` (streaming SSE).

**Documentación upstream pendiente:** el PR [openclaw/openclaw#42731](https://github.com/openclaw/openclaw/pull/42731) propone añadir la guía de proveedor en la doc oficial de OpenClaw (estado del PR: verificar en GitHub si ya está mergeado).

---

### B) `openclaw-cursor-brain` (plugin OpenClaw + MCP)

| Recurso | Enlace |
|--------|--------|
| Repositorio | [github.com/andeya/openclaw-cursor-brain](https://github.com/andeya/openclaw-cursor-brain) |
| Paquete npm | [npmjs.com/package/openclaw-cursor-brain](https://www.npmjs.com/package/openclaw-cursor-brain) |

**Instalación resumida:**

```bash
openclaw plugins install openclaw-cursor-brain
openclaw gateway restart
openclaw cursor-brain doctor
openclaw cursor-brain setup   # si no hubo TTY en el install
```

En versiones recientes de OpenClaw el instalador puede **bloquear** el plugin por patrones `child_process` / red (falso positivo de seguridad). Si ocurre, el propio CLI ofrece:

`openclaw plugins install openclaw-cursor-brain --dangerously-force-unsafe-install`

(úsalo solo si confías en el paquete y entiendes el riesgo).

**Puerto del proxy integrado (por defecto):** **18790** → `http://127.0.0.1:18790/v1`.

**Diferencia clave frente a (A):** además del proxy streaming, registra **MCP** para que **Cursor IDE** invoque herramientas del Gateway OpenClaw (`~/.cursor/mcp.json`). Sesiones persistidas, `scriptHash` en health, comandos `openclaw cursor-brain proxy *`.

**Config orientativa** (del README del plugin; validar contra tu versión de OpenClaw):

- Proveedor tipo `cursor-local` con `api: "openai-completions"`, `baseUrl` al proxy, lista `models` alineada con `agent --list-models`.
- `agents.defaults.model.primary` p. ej. `cursor-local/auto` y fallbacks en el mismo prefijo.

---

## Puertos y estabilidad

| Servicio | Puerto | Estado recomendado |
|----------|--------|---------------------|
| OpenClaw Gateway (loopback) | **18789** | Activo |
| Proxy `cursor-agent-api-proxy` | **4646** | **Activo (recomendado)** |
| Proxy `openclaw-cursor-brain` | **18790** | Deshabilitado (ver nota) |

**Nota sobre cursor-brain (18790):** en OpenClaw 2026.4.2 + cursor-brain 1.5.4, el plugin genera un bucle de reinicio del gateway (escribe modelos en `openclaw.json` -> gateway detecta cambio -> SIGUSR1 -> reinicio -> proxy muere -> repite). El proxy npm en **4646** es estable y se recomienda como `baseUrl` del proveedor `cursor-local`. Detalle en [SPIKE_CURSOR_OPENCLAW.md](SPIKE_CURSOR_OPENCLAW.md).

---

## Otras referencias comunitarias

- [pwnapplehat/cursor-proxy-patched](https://github.com/pwnapplehat/cursor-proxy-patched) — fork con parches (tool calling).
- [anyrobert/cursor-api-proxy](https://github.com/anyrobert/cursor-api-proxy) — otro proxy OpenAI-compatible.
- [Composio — Cursor + OpenClaw](https://composio.dev/toolkits/cursor/framework/openclaw) — toolkit MCP/OAuth.
- [OpenClaw — Model providers](https://docs.openclaw.ai/concepts/model-providers) — contrato general de proveedores.

---

## Coexistencia con Ollama (Jarvis)

En despliegues con **Ollama local** (ver [CIERRE_MODULO_OLLAMA_LOCAL.md](CIERRE_MODULO_OLLAMA_LOCAL.md)), Cursor vía proxy/plugin puede entrar como **otro candidato** en `primary` / `fallbacks` de `~/.openclaw/openclaw.json`, según prioridad que definas (p. ej. local primero, Cursor como refuerzo o al revés).

Si el **Gateway** corre bajo **systemd usuario**, revisa que `PATH` de la unidad incluya **`~/.local/bin`** (donde suele vivir `agent` tras el instalador oficial); si no, el plugin no localizará el CLI. Detalle en [SPIKE_CURSOR_OPENCLAW.md](SPIKE_CURSOR_OPENCLAW.md).

---

## Resultado de spikes en este repo

Resumen reproducible de pruebas locales (abril 2026, host Linux):

- [`docs/SPIKE_CURSOR_OPENCLAW.md`](SPIKE_CURSOR_OPENCLAW.md)
