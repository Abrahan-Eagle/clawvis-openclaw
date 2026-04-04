# clawvis-openclaw

Respaldo unificado del trabajo alrededor de **OpenClaw**, **Jarvis**, **Agent Town** y coordinación local (Scrum / Trello / Discord).

## Estructura del repositorio

| Carpeta | Contenido |
|---------|-----------|
| `jarvis-ecosystem/` | Automations, agents, skills, scripts, docs del ecosistema Jarvis |
| `documentos-jarvis-openclaw/` | Coordinación y notas en `Documentos` (gestión por fecha) |
| `openclaw-state/` | Copia de `~/.openclaw` (config, credenciales, workspace, agents de estado) |
| `agent-town/` | Proyecto Agent Town (Next); `node_modules` y `.next` no se versionan |
| `deploy/systemd/` | Copia de referencia del unit `openclaw-gateway.service` |
| `descargas-openclaw/` | Descargas relacionadas (opcional) |

**Seguridad:** este repo puede contener **secretos**. Debe ser **privado** en GitHub. Los servicios en ejecución siguen usando `~/.jarvis-ecosystem`, `~/.openclaw` y `~/agent-town` en disco; esta copia es para versionado y respaldo.

## Puesta en marcha (Linux, máquina actual)

1. **Node.js 22+** (OpenClaw lo exige): con nvm, `nvm install 22` y `nvm alias default 22`. En `~/.bashrc` ya se puede cargar `nvm use 22` en silencio tras `nvm.sh`.
2. **OpenClaw global:** `npm install -g openclaw@latest` usando el Node 22 de nvm.
3. **Config en vivo:** copiar o enlazar `~/.openclaw` desde `openclaw-state/` y ajustar rutas (`/home/TU_USUARIO`). En el navegador embebido, `browser.executablePath` debe apuntar a un Chrome/Chromium instalado (ej. `/usr/bin/google-chrome`).
4. **Ecosistema Jarvis:** `ln -sfn /ruta/al/repo/jarvis-ecosystem ~/.jarvis-ecosystem`.
5. **Gateway (systemd usuario):** copiar `deploy/systemd/openclaw-gateway.service` a `~/.config/systemd/user/`, revisar rutas de `node` y `openclaw/dist/index.js`, luego `systemctl --user daemon-reload`, `enable --now openclaw-gateway`. Puerto por defecto **18789** (loopback).
6. **Agent Town:** `cd agent-town && pnpm install && pnpm dev` → UI en **http://localhost:3000** (proxy al gateway `ws://127.0.0.1:18789/`).

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
| **Agent Town** | No arranca solo por defecto. Ejemplo opcional: [`deploy/systemd/agent-town-dev.service.example`](deploy/systemd/agent-town-dev.service.example) (modo `pnpm dev`; ajusta rutas). |

## Modelos LLM (ligero vs profundo, fallbacks, idle)

OpenClaw **no** trae un modo “Auto” por tarea como Cursor: `primary` + `fallbacks` solo cambian de modelo ante **fallos** (401, rate limit, etc.), no ante “pregunta difícil”. Para acercarse a “más potente cuando amerita”:

- **`jarvis`:** modelo **ligero** por defecto en `agents.defaults` (rápido/barato); cadena de `fallbacks` para resiliencia.
- **`jarvis-deep`:** mismo workspace que `jarvis`, modelo **más capaz** como `primary` (p. ej. OpenCode Nemotron primero); úsalo vía CLI o añade un `binding` específico a un chat.

Detalle, matriz y consumo en reposo: [docs/MODELOS_JARVIS_OPENCLAW.md](docs/MODELOS_JARVIS_OPENCLAW.md).

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
- Canales: `openclaw channels status` (y `--probe`).
- Turno de agente vía gateway: `openclaw agent --agent jarvis --message "hola"` (requiere API keys de modelo válidas en `auth-profiles` / proveedores).
- Modo profundo (mismo ecosistema, modelo más fuerte): `openclaw agent --agent jarvis-deep --message "…"`.

Si las sesiones heredaron rutas de otro usuario (`/home/will/...`), conviene normalizar rutas en `~/.openclaw/agents/*/sessions/` o regenerar sesiones.

## Sincronizar desde el equipo (referencia)

Tras cambios locales, desde `~/clawvis-openclaw`: `git add -A`, `git commit`, `git push origin main`.
