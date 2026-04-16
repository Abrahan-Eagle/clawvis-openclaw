# Troubleshooting: Composio + OpenClaw (`MCP client connection failed: fetch failed`)

## Contexto

Tras `openclaw composio doctor` puede aparecer:

- **Status: healthy** y listado de las **7 herramientas** `COMPOSIO_*`
- Inmediatamente despues: **`[plugins] [composio] MCP client connection failed: fetch failed`**

Eso **no** implica solo por si mismo que Composio o la consumer key esten mal: el plugin usa **mas de un flujo de red** (doctor vs cliente MCP remoto). Documentacion Composio sobre MCP: [Troubleshooting MCP](https://docs.composio.dev/docs/troubleshooting/mcp).

---

## Criterio de exito operativo (lo que importa)

El criterio correcto **no** es que desaparezca la ultima linea del doctor, sino:

- Con el **gateway** en ejecucion, el agente puede invocar herramientas Composio (p. ej. `COMPOSIO_SEARCH_TOOLS`, `COMPOSIO_MULTI_EXECUTE_TOOL`) y ejecutar acciones de toolkits (Canva, etc.) **sin error de red persistente**.

Si eso funciona, el mensaje al final del `doctor` puede ser **advertencia al cerrar** la sesion MCP secundaria; sigue siendo util actualizar el plugin OpenClaw cuando haya versiones nuevas.

---

## Fase 0: Clasificar (falso positivo vs fallo real)

1. Arrancar el **gateway** (`openclaw gateway` o servicio systemd).
2. Desde el **chat** (Telegram, Discord, TUI), pedir al agente una prueba minima:
   - Buscar herramientas Canva via Composio, o ejecutar una accion trivial del toolkit.
3. **Si las herramientas responden:** tratar el aviso post-doctor como **no bloqueante** para el pipeline Jarvis; documentar en incidencias internas si hace falta.
4. **Si el chat falla con `fetch failed` u otro error de red** en herramientas Composio: seguir Fase 1.

Script opcional (solo lectura de red): [../scripts/composio-diagnose.sh](../scripts/composio-diagnose.sh).

---

## Fase 1: Mitigaciones locales

### 1. Dashboard Composio

- Revisar si el proyecto tiene **`require_mcp_api_key`** u opciones que exijan cabeceras en el servidor MCP; alinear con [Troubleshooting MCP](https://docs.composio.dev/docs/troubleshooting/mcp) (401 / `x-api-key`).
- Confirmar que **Canva** (u otras apps) aparecen como conectadas y **ACTIVE** para el usuario esperado.

### 2. Proxy

Algunas herramientas no heredan el mismo proxy que los canales. Patron comentado en OpenClaw:

- Issues: [openclaw#3898](https://github.com/openclaw/openclaw/issues/3898), duplicado [openclaw#2102](https://github.com/openclaw/openclaw/issues/2102).
- Definir `HTTP_PROXY` y `HTTPS_PROXY` en el **entorno del proceso del gateway** (p. ej. unidad systemd `~/.config/systemd/user/openclaw-gateway.service`), no solo en la shell interactiva.
- Variable util en Node: `NODE_USE_ENV_PROXY=1` (tras cambios: `systemctl --user daemon-reload` y `openclaw gateway restart`).
- Si hay proxy tipo HTTP y sigue fallando, probar **modo tunel** del cliente proxy (comentarios en #3898).

### 3. Actualizar

```bash
openclaw plugins install --dangerously-force-unsafe-install @composio/openclaw-plugin
openclaw gateway restart
```

Guia Composio: [How to integrate Composio MCP with OpenClaw](https://composio.dev/toolkits/composio/framework/openclaw).

### 4. MCP Inspector

Para aislar **cliente vs servidor**, usar [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) contra la URL MCP de Composio (`https://connect.composio.dev/mcp`) con las cabeceras que indique vuestra cuenta. Si Inspector falla igual que OpenClaw, el problema puede estar en proyecto Composio o red; si Inspector va bien y OpenClaw no, escalar a OpenClaw (Fase 3).

---

## Fase 3: Escalacion upstream (si el runtime falla)

Abrir o ampliar un issue en **openclaw/openclaw** o contactar **Composio** ([support@composio.dev](mailto:support@composio.dev) / Discord en [docs](https://docs.composio.dev/docs/troubleshooting/mcp)) con:

| Dato | Contenido |
|------|-----------|
| Version OpenClaw | Salida de `openclaw --version` o banner del CLI |
| Version plugin | `plugins.installs.composio.resolvedVersion` en `~/.openclaw/openclaw.json` |
| Sintoma | Doctor healthy + linea `fetch failed` / o error solo en gateway |
| Red | Resultado de [composio-diagnose.sh](../scripts/composio-diagnose.sh) y si `node -e "fetch('https://connect.composio.dev/mcp')"` devuelve 401 |
| Proxy | Si aplica, y si `NODE_USE_ENV_PROXY` esta en el servicio del gateway |
| Inspector | Si la sesion MCP reproduce fuera de OpenClaw |

---

## Enlaces rapidos

| Recurso | URL |
|---------|-----|
| Composio MCP troubleshooting | https://docs.composio.dev/docs/troubleshooting/mcp |
| OpenClaw fetch failed + proxy (#3898) | https://github.com/openclaw/openclaw/issues/3898 |
| OpenClaw proxy discussion (#2102) | https://github.com/openclaw/openclaw/issues/2102 |
| Composio + OpenClaw | https://composio.dev/toolkits/composio/framework/openclaw |

---

## Historial

- **2026-04-16:** Documento inicial: doctor vs cliente MCP, criterio de exito, fases 0/1/3, enlaces GitHub y Composio.
