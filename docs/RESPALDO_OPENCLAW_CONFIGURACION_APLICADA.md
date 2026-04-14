# Respaldo: configuración OpenClaw + Cursor (host aplicada, abril 2026)

Documento para **no perder el hilo** de lo que quedó operativo en la máquina de referencia (`aipp`, Linux).  
**No incluye secretos:** nunca pegues aquí tokens reales. Los valores sensibles viven solo en `~/.openclaw/.env` y en BotFather / Discord Developer Portal.

---

## 1. Qué archivos son la “fuente de verdad” en el disco

| Ubicación | Qué es | ¿En git del proyecto? |
|-----------|--------|------------------------|
| `~/.openclaw/openclaw.json` | Config principal OpenClaw (agentes, canales, modelos, plugins) | **No** (está en HOME) |
| `~/.openclaw/.env` | Tokens y claves (`TELEGRAM_BOT_TOKEN`, Discord, `CURSOR_API_KEY`, etc.) | **No** — no commitear |
| `~/.config/systemd/user/openclaw-gateway.service` | Unidad usuario del gateway | **No** |
| `~/.config/systemd/user/cursor-agent-api.service` | Unidad usuario del proxy Composer | **No** |
| `/tmp/openclaw/openclaw-YYYY-MM-DD.log` | Logs del día (rotativos por fecha) | No |

**Respaldo físico recomendado** (fuera de git, con fecha):

```bash
mkdir -p ~/Backups/openclaw
cp -a ~/.openclaw/openclaw.json ~/Backups/openclaw/openclaw-$(date +%F).json
# Opcional cifrado o disco externo para una copia de .env (solo tú):
# cp -a ~/.openclaw/.env ~/Backups/openclaw/.env.$(date +%F)
cp -a ~/.config/systemd/user/openclaw-gateway.service ~/Backups/openclaw/
cp -a ~/.config/systemd/user/cursor-agent-api.service ~/Backups/openclaw/
```

Este archivo en `clawvis-openclaw/docs/` **sí** va en git: describe y reproduce la configuración **sin secretos**.

---

## 2. Regla crítica: `plugins.allow` y canales de chat

Si `plugins.allow` es un array **no vacío**, OpenClaw desactiva cualquier plugin cuyo **id** no esté en la lista **antes** de aplicar otras reglas. Eso dejaba Telegram / Discord / WhatsApp “muertos” aunque `channels.*.enabled` fuera `true`.

**Ids de plugin alineados a canales usados** (nombres oficiales en extensiones bundled):

- `telegram`
- `discord`
- `whatsapp`
- `browser` (automatización navegador)

**Estado aplicado** (resumen): `plugins.allow` incluye los cuatro anteriores. Sin eso, `openclaw channels list` podía mostrar canales vacíos o el transporte no arrancaba.

---

## 3. Fragmento de `openclaw.json` (referencia, sin secretos)

Copia conceptual para restaurar a mano si perdieras el archivo. Ajusta rutas de `workspace` si cambias de usuario o máquina.

**Canales y políticas (ejemplo aplicado):**

```json
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "dmPolicy": "pairing",
      "groupPolicy": "allowlist",
      "debounceMs": 0,
      "mediaMaxMb": 50
    },
    "discord": {
      "enabled": true,
      "dmPolicy": "open",
      "groupPolicy": "open",
      "allowFrom": ["*"]
    },
    "telegram": {
      "enabled": true,
      "dmPolicy": "pairing",
      "groupPolicy": "open",
      "mediaMaxMb": 50
    }
  },
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "loopback",
    "auth": { "mode": "none" },
    "tailscale": { "mode": "off", "resetOnExit": false }
  },
  "plugins": {
    "entries": {
      "browser": { "enabled": true, "config": {} }
    },
    "installs": {},
    "allow": ["browser", "telegram", "discord", "whatsapp"]
  },
  "models": {
    "mode": "merge",
    "providers": {
      "cursor-local": {
        "baseUrl": "http://127.0.0.1:4646/v1",
        "apiKey": "not-needed",
        "api": "openai-completions"
      }
    }
  }
}
```

**Notas:**

- `apiKey` **`not-needed`** es el valor esperado por `cursor-agent-api-proxy` en local (no uses `"local"` si el proxy falla al validar).
- El archivo real en disco tiene además `agents`, `bindings`, listas largas de modelos, `browser` con Chrome, etc.; para recuperación total usa la copia fechada de `openclaw.json`, no solo este fragmento.
- **Browser / CDP (Chrome ≥111):** en `browser.extraArgs` conviene `"--remote-allow-origins=*"`; opcional `"--remote-debugging-address=127.0.0.1"`. Opcional en `browser`: `"cdpUrl": "http://127.0.0.1:18800"` para fijar host/puerto del probe. Tras un fallo de arranque, `curl` al puerto puede dar error porque OpenClaw mata el proceso. Si usas proxy global, el unit del gateway puede definir `NO_PROXY=127.0.0.1,localhost,::1` y variables `HTTP(S)_PROXY`/`ALL_PROXY` vacías.
- **Causa típica del falso fallo CDP (`DevTools listening` pero el probe nunca pasa):** el directorio de perfil `~/.openclaw/browser/<perfil>/user-data` está **corrupto o incompatible**: Chrome imprime la línea de DevTools y **sale al instante** (p. ej. código de salida 133). No es un problema de timeout del HTTP client. **Solución:** `openclaw browser reset-profile` o mover ese `user-data` a un respaldo y dejar que OpenClaw cree uno nuevo. Revisar también `SingletonLock` / `SingletonSocket` rotos en ese árbol si hubo cierres bruscos.
- **Parches locales (abr 2026, host `aipp`)** en `node_modules/openclaw` (se pierden con `npm i -g openclaw@latest`): **(1)** `routes-D3B9A956.js`: `cdpProbeMs` **5000 ms**, `CHROME_LAUNCH_READY_WINDOW_MS` **60 s**, y (si aplica en tu build) URL CDP derivada/`cdpUrlForPort` coherentes con `localhost` vs `127.0.0.1`. **(2)** `runtime-api-DN3n8SWI.js`: `BROWSER_MANAGE_REQUEST_TIMEOUT_MS` subido a **120 s** para que `openclaw browser open` no haga timeout a los **45 s** fijos mientras el gateway tarda hasta ~60 s en el arranque de Chrome. **(3)** Systemd `openclaw-gateway.service`: proxy vacío + `NO_PROXY` loopback como arriba.

**Bindings a agente `jarvis` (canales):** whatsapp (`accountId: *`), discord (`guildId: *`), telegram (`accountId: *`).

---

## 4. Proveedor Cursor vía proxy npm (puerto 4646)

- **Paquete:** `cursor-agent-api-proxy` (global npm).
- **Puerto:** `4646` (por defecto).
- **Decisión documentada en el spike:** preferido frente a `openclaw-cursor-brain` en `18790` por bucles de reinicio del gateway al reescribir config.

**Comprobación rápida:**

```bash
curl -sS http://127.0.0.1:4646/v1/models
```

Si falla: asegúrate de sesión Cursor (`agent login` o `CURSOR_API_KEY`) y de que **solo un proceso** escuche en 4646 (`EADDRINUSE` si hay duplicado).

---

## 5. Systemd (usuario): unidades tal como quedaron

En el repo [`deploy/systemd/`](../deploy/systemd/) hay copia de referencia del gateway (con `PATH` que incluye `~/.local/bin`) y el ejemplo [`cursor-agent-api.service.example`](../deploy/systemd/cursor-agent-api.service.example) para el proxy en 4646.

### `openclaw-gateway.service`

Ruta: `~/.config/systemd/user/openclaw-gateway.service`

```ini
[Unit]
Description=OpenClaw Gateway (user)
After=network-online.target
Wants=network-online.target

[Service]
EnvironmentFile=-%h/.openclaw/.env
ExecStart=/home/aipp/.nvm/versions/node/v22.22.2/bin/node /home/aipp/.nvm/versions/node/v22.22.2/lib/node_modules/openclaw/dist/index.js gateway --port 18789
Restart=always
RestartSec=5
TimeoutStopSec=30
TimeoutStartSec=60
SuccessExitStatus=0 143
KillMode=control-group
Environment=HOME=/home/aipp
Environment=TMPDIR=/tmp
Environment=NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
Environment=PATH=/home/aipp/.local/bin:/home/aipp/.nvm/versions/node/v22.22.2/bin:/usr/local/bin:/usr/bin:/bin
Environment=OPENCLAW_GATEWAY_PORT=18789
Environment=OPENCLAW_SYSTEMD_UNIT=openclaw-gateway.service
Environment=OPENCLAW_SERVICE_MARKER=openclaw
Environment=OPENCLAW_SERVICE_KIND=gateway

[Install]
WantedBy=default.target
```

**Importante:**

- `EnvironmentFile=-%h/.openclaw/.env` carga variables para el gateway (tokens, etc.). La ruta debe ser válida; evita rutas mal formadas tipo `~/home/usuario/...`.
- `PATH` incluye **`~/.local/bin`** para que el proceso encuentre el CLI `agent` de Cursor si hace falta.

### `cursor-agent-api.service`

Ruta: `~/.config/systemd/user/cursor-agent-api.service`

```ini
[Unit]
Description=Cursor Agent API Proxy
After=network.target

[Service]
Type=simple
ExecStart=/home/aipp/.nvm/versions/node/v22.22.2/bin/node /home/aipp/.nvm/versions/node/v22.22.2/lib/node_modules/cursor-agent-api-proxy/dist/server/standalone.js run
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

**Orden recomendado al arrancar sesión gráfica/SSH:** proxy en 4646 antes o a la par del gateway (el gateway tolera reintentos de modelo).

```bash
systemctl --user daemon-reload
systemctl --user enable --now cursor-agent-api.service
systemctl --user enable --now openclaw-gateway.service
```

---

## 6. Variables de entorno (solo nombres; valores en tu `.env` privado)

Según lo usado en el flujo Telegram / Discord / OpenClaw, tu `~/.openclaw/.env` puede incluir (ejemplos de nombres típicos — **comprueba con tu archivo real**):

- `TELEGRAM_BOT_TOKEN`
- Variables de Discord si aplica (token de bot / app, según doc OpenClaw para `channels add discord --use-env`)
- `CURSOR_API_KEY` (opcional si usas login interactivo del CLI en su lugar)

**No subas `.env` a git.** Para compartir con otro equipo, usa un `.env.example` con líneas vacías o placeholders.

---

## 7. Comandos útiles post-restore

```bash
export PATH="/home/aipp/.nvm/versions/node/v22.22.2/bin:$PATH"
openclaw channels list
openclaw pairing list telegram
systemctl --user status openclaw-gateway.service cursor-agent-api.service
```

**Telegram + `dmPolicy: pairing`:** los DMs nuevos requieren aprobar el código que envía el flujo de pairing (`openclaw pairing approve ...`), no el hash del banner de versión.

---

## 8. Documentos relacionados en este repo

- [`SPIKE_CURSOR_OPENCLAW.md`](SPIKE_CURSOR_OPENCLAW.md) — spike, puertos, decisión 4646 vs 18790.
- [`PROVEEDOR_CURSOR_OPENCLAW.md`](PROVEEDOR_CURSOR_OPENCLAW.md)
- [`MODELOS_JARVIS_OPENCLAW.md`](MODELOS_JARVIS_OPENCLAW.md)

---

---

## 9. Memoria avanzada (MemPalace, abr 2026)

- **MemPalace 3.0.0** instalado via `pipx install mempalace`.
- Palace en `~/.mempalace/palace/` (ChromaDB local, ~200 MB).
- Knowledge Graph en `~/.mempalace/knowledge_graph.sqlite3` (54 triples del ecosistema).
- MCP Server registrado en `openclaw.json` bajo `mcp.servers.mempalace`.
- **OpenClaw memory-core activado:** provider `ollama` con modelo `nomic-embed-text`, session-memory hook habilitado, memoryFlush pre-compaction activo, hybrid search (vector 0.7 + FTS 0.3).
- Auto-mine systemd timer: `mempalace-auto-mine.timer` (cada 30 min).
- Documentacion completa: `jarvis-ecosystem/docs/MEMORIA_MEMPALACE.md`.
- **Cierre del módulo y procedimiento de réplica desde Git:** `jarvis-ecosystem/docs/MODULO_MEMPALACE_CIERRE.md` — incluye checklist, backup de `~/.mempalace`, artefactos en `deploy/mempalace/`.

---

---

## 10. Forense Paperclip — patrones adoptados (abr 2026)

- **Goals formalizados:** `jarvis-ecosystem/GOALS.md` con IDs `G-H01..G-J02`, metricas y reglas de alineacion.
- **Organigrama:** `jarvis-ecosystem/ORG_CHART.md` (diagrama Mermaid con goals por agente).
- **Heartbeats operativos:** activados en `openclaw.json` para jarvis (30m), sales-hunter (1h), mkt-content (2h). Checklists en `agents/*/HEARTBEAT.md`. Guia: `docs/HEARTBEAT_OPERATIVO.md`.
- **Cost tracking:** `scripts/cost-report.sh` parsea sesiones JSONL y genera reporte mensual por agente.
- **Approval Gates:** `docs/APPROVAL_GATES.md` con 10 gates formales (AG-01..AG-10); referenciados en AGENTS.md de cada workspace.
- **Rutinas documentadas con Goals:** tabla completa en `CLAWFLOWS.md` seccion "Registro completo de rutinas".
- **Resumen forense:** `docs/FORENSE_PAPERCLIP_RESUMEN.md`.

---

---

## 11. Forense Superpowers — metodologia y skills (abr 2026)

- **Plugin Superpowers v5.0.7** instalado en Cursor (`~/.cursor/plugins/local/superpowers/`, git clone).
- **4 skills adaptados** creados en `agents/jarvis/skills/`:
  - `brainstorming-ops/SKILL.md` — brainstorming obligatorio antes de tareas complejas.
  - `verification-before-completion/SKILL.md` — evidencia antes de claims.
  - `systematic-debugging/SKILL.md` — 4 fases, root cause primero.
  - `dev-methodology/SKILL.md` — TDD + planes + code review (listo para dev-agency).
- **AGENTS.md actualizados** (jarvis, ventas, marketing) con seccion "Protocolo de calidad (Superpowers)".
- Documentacion: `docs/FORENSE_SUPERPOWERS_RESUMEN.md`.

---

**Ultima actualizacion del respaldo en repo:** 2026-04-14 (forense Superpowers: skills de calidad, plugin Cursor, protocolo en AGENTS.md).
