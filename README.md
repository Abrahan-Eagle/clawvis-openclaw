# clawvis-openclaw

Respaldo unificado del trabajo alrededor de **OpenClaw**, **Jarvis**, **Agent Town** y coordinación local (Scrum / Trello / Discord).

## Estructura del repositorio

| Carpeta | Contenido |
|---------|-----------|
| `jarvis-ecosystem/` | Automations, agents, skills, scripts, docs del ecosistema Jarvis |
| `documentos-jarvis-openclaw/` | Coordinación y notas en `Documentos` (gestión por fecha) |
| `openclaw-state/` | Copia de `~/.openclaw` (config, credenciales, workspace, agents de estado) |
| `agent-town/` | Proyecto Agent Town (Next); `node_modules` y `.next` no se versionan |
| `deploy/systemd/` | Referencia: `openclaw-gateway.service`, `cursor-agent-api.service.example`, `agent-town-dev.service.example` |
| `descargas-openclaw/` | Descargas relacionadas (opcional) |

**Seguridad:** este repo puede contener **secretos**. Debe ser **privado** en GitHub. Los servicios en ejecución siguen usando `~/.jarvis-ecosystem`, `~/.openclaw` y `~/agent-town` en disco; esta copia es para versionado y respaldo.

## Puesta en marcha (Linux, máquina actual)

1. **Node.js 22+** (OpenClaw lo exige): con nvm, `nvm install 22` y `nvm alias default 22`. En `~/.bashrc` ya se puede cargar `nvm use 22` en silencio tras `nvm.sh`.
2. **OpenClaw global:** `npm install -g openclaw@latest` usando el Node 22 de nvm.
3. **Config en vivo:** copiar o enlazar `~/.openclaw` desde `openclaw-state/` y ajustar rutas (`/home/TU_USUARIO`). En el navegador embebido, `browser.executablePath` debe apuntar a un Chrome/Chromium instalado (ej. `/usr/bin/google-chrome`).
4. **Ecosistema Jarvis:** `ln -sfn /ruta/al/repo/jarvis-ecosystem ~/.jarvis-ecosystem`.

   **Coherencia con OpenClaw:** en `~/.openclaw/openclaw.json`, los agentes (`agents.list`) suelen apuntar el `workspace` a rutas bajo `/home/TU_USUARIO/jarvis-ecosystem/agents/...`. Eso **debe resolver al mismo árbol** que `jarvis-ecosystem/` del repo (vía el enlace simbólico). Comprueba con `readlink -f ~/.jarvis-ecosystem` y compáralo con la ruta absoluta del repo; si editas solo el clon en `/var/www/...` pero OpenClaw apunta a otra copia, perderás cambios en GitHub.

5. **Proxy Cursor (opcional recomendado):** copiar [`deploy/systemd/cursor-agent-api.service.example`](deploy/systemd/cursor-agent-api.service.example) a `~/.config/systemd/user/cursor-agent-api.service`, ajustar rutas de `node` y del módulo `cursor-agent-api-proxy`, luego `daemon-reload` y `enable --now`. Debe haber **un solo** listener en el puerto **4646** (si ya corres el proxy a mano, systemd fallará con `EADDRINUSE`).

6. **Gateway (systemd usuario):** copiar `deploy/systemd/openclaw-gateway.service` a `~/.config/systemd/user/`, revisar rutas de `node` y `openclaw/dist/index.js`, luego `systemctl --user daemon-reload`, `enable --now openclaw-gateway`. Puerto por defecto **18789** (loopback).
7. **Agent Town:** `cd agent-town && pnpm install && pnpm dev` → UI en **http://localhost:3000** (proxy al gateway `ws://127.0.0.1:18789/`). Ejecuta el dev server con el **mismo usuario Linux** que el gateway para que `/api/agents/discover` lea `~/.openclaw` correcto. Si el Terminal o el chat dicen “Not connected”, abre el panel **Connection** (icono del enchufe en el dock) y pulsa **Connect**; la URL por defecto suele ser `ws://localhost:3000/api/gateway` (túnel al OpenClaw en 18789). Con `gateway.auth.mode: none`, el token puede ir vacío. Tras un primer login correcto, la app guarda la config en `localStorage`. En builds recientes, OpenClaw intenta **auto-conectar** al cargar si aún no hay config guardada.

Si las tareas en Agent Town pasan a **FAILED** al instante con `Assign failed` en el chat, revisa el log del gateway: versiones recientes de OpenClaw rechazan propiedades extra en `chat.send`. El front ya no envía `seatLabel`/`seatRole` salvo proveedor **Auggie**.

Perfil CDP del navegador en el repo: `openclaw-state/browser/openclaw/user-data` → enlace a `~/.openclaw/cdp-user-data` (evita rutas de otro usuario).

## Telegram (OpenClaw)

Documentación oficial: [channels/telegram](https://docs.openclaw.ai/channels/telegram).

1. Crea un bot con **@BotFather** (`/newbot`) y copia el **token**.
2. En **`~/.openclaw/.env`** define `TELEGRAM_BOT_TOKEN=<token>` (no subas este archivo a Git).
3. En **`~/.openclaw/openclaw.json`** debe existir `channels.telegram` con `enabled: true` y `dmPolicy` (por defecto **pairing** para el primer contacto).
4. Enlaza mensajes al agente con `bindings` (`channel: "telegram"`, `accountId: "*"` → agente `jarvis` si aplica).
5. Reinicia el gateway: `systemctl --user restart openclaw-gateway`.
6. **Pairing (DM):** escribe al bot en Telegram; en el PC ejecuta `openclaw pairing list telegram` y `openclaw pairing approve telegram <CÓDIGO>` (el código caduca en ~1 h).
7. Comprueba: `openclaw channels status` (Telegram debe pasar de `not configured` a conectado cuando el token es válido).

Grupos: revisa *privacy mode* del bot en BotFather (`/setprivacy`) y opcionalmente `channels.telegram.groups` en la doc.

## Arranque al iniciar sesión (resumen)

| Servicio | Comportamiento |
|----------|----------------|
| **OpenClaw gateway** | `systemctl --user enable --now openclaw-gateway` — suele arrancar al **iniciar sesión** en el escritorio (systemd --user). |
| **Sin login gráfico** | Opcional: `sudo loginctl enable-linger $USER` para que los servicios `--user` existan tras boot (útil en servidores headless). |
| **Agent Town** | No arranca solo por defecto. Para dejarlo al iniciar sesión: copiar [`deploy/systemd/agent-town-dev.service.example`](deploy/systemd/agent-town-dev.service.example) a `~/.config/systemd/user/agent-town-dev.service`, ajustar rutas, `daemon-reload`, `enable --now`. Manual: `cd agent-town && pnpm dev` → **http://localhost:3000**. |

## Modelos LLM (qué manda en la práctica)

La **fuente de verdad** del modelo que usan Telegram, Discord y el agente por defecto es **`agents.defaults.model`** y el bloque `model` de cada entrada en **`agents.list`** dentro de `~/.openclaw/openclaw.json`. Lo que leas aquí o en el router YAML es orientación; lo que esté en ese JSON es lo que ejecuta el gateway.

- **Patrón actual en este equipo (ejemplo):** proveedor **`cursor-local`** con `primary` tipo **`cursor-local/composer-2-fast`** y API en **`http://127.0.0.1:4646/v1`** (`cursor-agent-api-proxy`). Ver [docs/PROVEEDOR_CURSOR_OPENCLAW.md](docs/PROVEEDOR_CURSOR_OPENCLAW.md) y [docs/SPIKE_CURSOR_OPENCLAW.md](docs/SPIKE_CURSOR_OPENCLAW.md).
- **Patrón alternativo (económico / sin Cursor):** `primary` en Groq, OpenCode, Ollama, etc., con `fallbacks` solo ante **error** de proveedor (401, rate limit, …). OpenClaw **no** tiene “Auto” por dificultad de la pregunta como Cursor.
- **`jarvis-deep`:** mismo workspace que `jarvis`, otro `model.primary` más capaz; CLI `openclaw agent --agent jarvis-deep` o `binding` más específico.
- **Router YAML** (`jarvis-ecosystem/agents/jarvis/scripts/`, [docs/MODELOS_JARVIS_OPENCLAW.md](docs/MODELOS_JARVIS_OPENCLAW.md)): útil en **terminal/scripts**; **no** sustituye el modelo en canales salvo que diseñes bindings o procesos aparte.

Detalle, matriz, router y consumo en reposo: [docs/MODELOS_JARVIS_OPENCLAW.md](docs/MODELOS_JARVIS_OPENCLAW.md).

## Documentación en `docs/`

| Documento | Contenido |
|-----------|-----------|
| [RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md](docs/RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md) | Respaldo **sin secretos**: systemd, fragmentos de `openclaw.json`, regla **`plugins.allow`**, proxy 4646, comandos de copia local. |
| [SPIKE_CURSOR_OPENCLAW.md](docs/SPIKE_CURSOR_OPENCLAW.md) | Spike Cursor + OpenClaw (Linux): CLI, gateway, puertos 18789 / 4646 / 18790. |
| [PROVEEDOR_CURSOR_OPENCLAW.md](docs/PROVEEDOR_CURSOR_OPENCLAW.md) | Guía del proveedor Cursor / OpenAI-compatible con OpenClaw. |
| [MODELOS_JARVIS_OPENCLAW.md](docs/MODELOS_JARVIS_OPENCLAW.md) | Modelos, agentes `jarvis` / `jarvis-deep`, fallbacks. |
| [OPENCLAW_FORENSE_RUNBOOK.md](docs/OPENCLAW_FORENSE_RUNBOOK.md) | Runbook forense OpenClaw. |
| [CIERRE_MODULO_OLLAMA_LOCAL.md](docs/CIERRE_MODULO_OLLAMA_LOCAL.md) | Notas Ollama local. |

**Aviso `plugins.allow`:** si en `openclaw.json` defines `plugins.allow` con una lista no vacía, debes incluir los IDs de cada canal que uses (`telegram`, `discord`, `whatsapp`, …) además de `browser`. Si no, el canal puede quedar desactivado aunque `channels.<id>.enabled` sea `true`. Detalle en el doc de respaldo.

## Qué queda en GitHub y qué no

- **En el repo (GitHub):** markdown de `docs/`, `deploy/systemd/`, `jarvis-ecosystem/`, etc. — útil para reproducir **procedimiento** y valores no sensibles.
- **No subir nunca:** `~/.openclaw/.env`, tokens de bots, API keys. El `openclaw.json` **completo** en HOME no se versiona aquí por defecto; para copia de seguridad usa backups locales fechados (ver sección “Respaldo físico” en el doc de respaldo) o la carpeta `openclaw-state/` del repo **solo si** mantienes el repo **privado** y aceptas el riesgo (el README ya advierte que puede contener secretos).
- Tras cambios en el equipo: `git add`, `commit`, `push` desde la raíz del repo.

## Pruebas rápidas (CLI)

- Gateway: `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:18789/` → `200`.
- Proxy Cursor: `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:4646/v1/models` → `200`.
- `plugins.allow`: `grep -A6 '"allow"' ~/.openclaw/openclaw.json` — deben figurar los plugins de cada canal habilitado (`telegram`, `discord`, `whatsapp`, …) y `browser` si aplica.
- Canales: `openclaw channels list` / `openclaw channels status` (y `--probe`).
- Turno de agente: `openclaw agent --agent jarvis --message "hola"` (requiere proveedor/modelo válidos según tu `openclaw.json` y `auth-profiles` si aplica).
- Modo profundo: `openclaw agent --agent jarvis-deep --message "…"`.

**Última pasada de checklist en el host de referencia (abr 2026):** enlace `~/.jarvis-ecosystem` → repo OK; `18789` y `4646` respondieron `200`; canales Telegram/Discord configurados; `openclaw agent --agent jarvis --message "ping"` respondió correctamente. Si `systemctl --user is-active cursor-agent-api` muestra `activating` pero `4646` responde, suele haber **otro** proceso ya escuchando en ese puerto (un solo proxy activo es suficiente).

Si las sesiones heredaron rutas de otro usuario (`/home/will/...`), conviene normalizar rutas en `~/.openclaw/agents/*/sessions/` o regenerar sesiones.

## Sincronizar desde el equipo (referencia)

Tras cambios locales, desde `~/clawvis-openclaw`: `git add -A`, `git commit`, `git push origin main`.
