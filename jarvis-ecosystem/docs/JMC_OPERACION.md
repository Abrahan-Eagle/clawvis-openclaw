# Jarvis Mission Control (JMC) — operación

## Requisitos

- Python 3.10+
- Repo `jarvis-ecosystem` en disco

### UI estática y DevTools (CSP / `eval`)

La UI en `jmc/ui/index.html` declara una **Content-Security-Policy** restrictiva (`script-src 'self'`). El código de JMC **no** usa `eval()` ni `new Function()`. Si Chrome u otro navegador muestra un aviso de *Content Security Policy blocks eval*, suele ser **ruido de extensiones** (React DevTools, etc.) inyectando scripts; no indica un fallo del adapter. Si desaparece en ventana de incógnito sin extensiones, puede ignorarse para JMC.

**API base y `connect-src`:** el meta CSP limita `connect-src` a `'self'` y loopback (`127.0.0.1` / `localhost`). La UI asume **mismo origen** que el adapter o API en loopback. Si en *Conexión* guardas una API base en otro host, las peticiones `fetch` pueden bloquearse por CSP: la solución operativa es servir la UI detrás del **mismo host** que la API (p. ej. reverse proxy) o generar/servir una política que incluya ese origen (no se amplía el meta por defecto; mantener CSP estricta).

La directiva **`frame-ancestors`** no tiene efecto en un `<meta http-equiv="Content-Security-Policy">`; solo aplica si el servidor envía la política en **cabecera HTTP**. Por eso no va en el meta de la UI: evita el aviso de DevTools *frame-ancestors is ignored when delivered via a meta element*. Si necesitas prohibir incrustar JMC en iframes de otros orígenes, habría que añadir `frame-ancestors 'none'` (u otra política) desde el adapter o el reverse proxy en la respuesta que sirve `/ui/`.

---

## Instalar

Desde la raíz del monorepo (donde está `jarvis-ecosystem/`):

```bash
cd jarvis-ecosystem
python3 -m venv .venv-jmc
. .venv-jmc/bin/activate
pip install -e jmc/adapter
```

### Tras `git pull` (adapter / dependencias)

Si actualizaste dependencias o el código del adapter, **reinstala el paquete en el venv** y reinicia el servicio; `jmc-start.sh` / `jmc-smoke.sh` fallan pronto si falta `import app.main` (p. ej. `python-multipart` u otras deps sin instalar):

```bash
cd jarvis-ecosystem
.venv-jmc/bin/pip install -e jmc/adapter
sudo systemctl reset-failed jmc-adapter   # si aplica
sudo systemctl restart jmc-adapter
```

---

## Variables de entorno

| Variable | Obligatorio | Descripción |
|----------|-------------|-------------|
| `JMC_BEARER_TOKEN` | Sí (≥32 caracteres) | Token Bearer para todas las rutas `/v1/*`. |
| `JMC_BIND` | No (default `127.0.0.1`) | Host de escucha. |
| `JMC_PORT` | No (default `8765`) | Puerto. |
| `JMC_UVICORN_BIN` | No | Ruta absoluta a `uvicorn` usada por `jmc-systemd-install.sh` al generar la unidad (también se lee del `EnvironmentFile` si ya existe al reinstalar). |
| `JMC_REPO_ROOT` | No | Raíz del repo `jarvis-ecosystem` si no se puede inferir. |
| `JMC_CORS_ORIGIN` | No | Orígenes permitidos CORS: **CSV** de URLs (hasta 16), ej. `http://127.0.0.1:8765,http://localhost:5173`. Vacío = sin middleware CORS. |
| `JMC_OPENCLAW_JSON_PATH` | No | **v1.10+** Ruta absoluta a `openclaw.json` (prioridad sobre `~/.openclaw/` y repo). Útil en tests/CI. |
| `JARVIS_AUTONOMY_MODE` | No | Override modo autonomía para `/v1/modes/current`. |
| `JMC_ALLOW_MODE_WRITE` | No | **Obsoleto (ignorado).** `POST /v1/modes/current` queda habilitado siempre que el cliente envíe Bearer válido. Puede quedar en ficheros antiguos sin efecto. |
| `JMC_OPENCLAW_ENV_PATH` | No | Ruta absoluta del archivo `.env` donde escribir `JARVIS_AUTONOMY_MODE` (default: `~/.openclaw/.env`) al usar **Aplicar** en la UI o el POST. |
| `JMC_BRAND_NAME` | No | Nombre corto en cabecera UI / título (default `JMC`). |
| `JMC_BRAND_EMOJI` | No | Emoji o glifo en sidebar (default `◆`). |
| `JMC_BRAND_AVATAR` | No | Reservado (URL o path no servido por el adapter hoy; ignorado si vacío). |
| `JMC_BRAND_COMPANY` | No | Subtítulo / compañía en sidebar. |
| `JMC_BRAND_OWNER` | No | Subtítulo / propietario en sidebar. |
| `JMC_AUTH_FAIL_MAX` | No | Tras N fallos **Bearer** o **inbound** (`X-JMC-Inbound-Secret`) por IP en la ventana, `429` (Bearer: `auth_locked`; inbound: `inbound_locked`). Mínimo efectivo `3`. Default `10`. |
| `JMC_AUTH_FAIL_WINDOW` | No | Ventana en segundos para el contador anterior (default `900`). |
| `JMC_RUNTIME_SERVICES` | No | CSV de nombres de unidades/servicios a inspeccionar con `systemctl` (vacío = lista vacía en API). **No** incluir servicios sensibles. |
| `JMC_RUNTIME_LOGS` | No | **v1.10** `1`/`true`: permite `journalctl` en `GET /v1/runtime/services?journal_lines<=20` (solo unidades listadas en `JMC_RUNTIME_SERVICES`). |
| `JMC_TASK_ZOMBIE_HOURS` | No | Umbral horas para `/v1/state/zombies` (default `72`, máx. `720`). |
| `JMC_MEMORY_STALE_DAYS` | No | Días sin tocar `MEMORY.md`/`SOUL.md` para marcar `stale` en `/v1/memory/list` (default `14`). |
| `JMC_EXT_HEALTHCHECKS` | No | CSV `nombre\|https://host/...,...` (máx. 8) para `GET /v1/external/healthchecks`. |
| `JMC_EXT_ALLOW_LOCAL` | No | `1`: permite comprobar URLs que resuelvan a loopback. |
| `JMC_WEBHOOK_URL` / `JMC_WEBHOOK_SECRET` | No | Webhook POST saliente (solo esquemas **`http`/`https`** con host; HMAC SHA-256 hex en cabecera `X-JMC-Signature` si hay secret). El host resuelto **no** puede ser IP privada, enlace local ni loopback salvo `JMC_WEBHOOK_ALLOW_LOCAL=1` (misma idea que `JMC_EXT_ALLOW_LOCAL` en healthchecks). |
| `JMC_WEBHOOK_ALLOW_LOCAL` | No | `1`/`true`: permite que `JMC_WEBHOOK_URL` resuelva a loopback (p. ej. pruebas locales). |
| `JMC_INBOUND_TELEGRAM_SECRET` | No | **≥16 caracteres.** Activa webhooks inbound (sin Bearer) junto con `JMC_INBOUND_CHANNEL_SECRET` (cualquiera de los dos basta). Ver sección *Canales inbound* más abajo. |
| `JMC_INBOUND_CHANNEL_SECRET` | No | **v1.11+** Opcional. Si está definido (≥16), tiene prioridad sobre `JMC_INBOUND_TELEGRAM_SECRET` como secreto único para **todos** los canales (`telegram`, `whatsapp`, `discord`). |
| `JMC_STATE_CACHE_TTL` | No | **v1.11+** Segundos de caché para lecturas repetidas de `state/tasks` y `state/handoffs` (default `4`, máx. `30`). |
| `JMC_STATE_DIR` | No | Raíz del directorio `state/` (tareas, handoffs, `activity-log.jsonl`). Si no se define, el adapter infiere la ruta del repo; debe alinearse con `JARVIS_STATE_DIR` del entorno que escribe el `activity-log` CLI. |
| `JMC_BRAND_DESCRIPTION` / `JMC_BRAND_LOCATION` / `JMC_BRAND_BIRTH_DATE` / `JMC_BRAND_TWITTER` | No | Campos cosméticos extra en `brand` (`social` = Twitter handle). |
| `JMC_CHAT_INBOX_DIR` | No | **Chat buzón** Raíz del buzón (default: `<state>/jmc-inbox`). Si es ruta absoluta, debe quedar bajo el **repo** o bajo **`state/`** resuelto; para otra ruta define `JMC_CHAT_INBOX_ALLOW_EXTERNAL=1` (riesgo explícito). |
| `JMC_CHAT_INBOX_ALLOW_EXTERNAL` | No | `1`/`true`: permite `JMC_CHAT_INBOX_DIR` fuera del repo/`state/` (auditoría operativa). |
| `JMC_CHAT_MAX_FILE_BYTES` | No | Tamaño máximo por adjunto en bytes (default `26214400` = 25 MiB; tope duro `104857600` = 100 MiB; mínimo efectivo `1024`). |
| `JMC_CHAT_MAX_FILES_PER_MSG` | No | Máximo de archivos por mensaje (default `5`, máx. `10`). |
| `JMC_CHAT_MIRROR_ENABLED` | No | `1`/`true`: habilita en la UI el checkbox de espejo a Telegram/Discord vía `openclaw message send`. |
| `JMC_CHAT_MIRROR_CHANNELS` | No | CSV de canales permitidos para el espejo (subset de `telegram`, `discord`; default `telegram,discord`). |
| `JMC_OPENCLAW_BIN` | No | **Chat espejo** Ruta al binario `openclaw` (default nombre `openclaw` en `PATH`). En el host del adapter debe existir el binario para que el espejo funcione; si no, el mensaje igual se guarda en disco y la API devuelve aviso `openclaw_bin_missing`. |

### Heartbeat por agente (`openclaw.json`)

La vista **Coverage** marca “sin heartbeat” si la entrada en `agents.list` **no** incluye un objeto no vacío `heartbeat`. Eso se configura en **`~/.openclaw/openclaw.json`** (no en el repo). Plantilla por agente (ajusta `every`, ventana y `timezone`):

```json
{
  "id": "mkt-content",
  "workspace": "/ruta/a/jarvis-ecosystem/agents/marketing",
  "heartbeat": {
    "every": "1h",
    "target": "none",
    "lightContext": true,
    "activeHours": {
      "start": "08:00",
      "end": "20:00",
      "timezone": "America/Caracas"
    }
  }
}
```

Copia el bloque `heartbeat` (y opcionalmente `activeHours`) en cada `id` que quieras vigilar; reinicia el gateway OpenClaw si hace falta para releer el JSON.

### Canales inbound → JMC (Activity)

Los bots (Telegram, WhatsApp, Discord, etc.) **no** escriben solos en JMC: hace falta que el **gateway** u otro script invoque el registro unificado.

1. Define **`JMC_INBOUND_CHANNEL_SECRET`** o **`JMC_INBOUND_TELEGRAM_SECRET`** (≥16) en el entorno del adapter.
2. En cada mensaje relevante, `POST` a **`/v1/webhooks/inbound/{channel}`** con `{channel}` ∈ `telegram` | `whatsapp` | `discord`, cabecera **`X-JMC-Inbound-Secret`**, y cuerpo JSON (mismo esquema para todos los canales), por ejemplo:
   ```json
   { "direction": "in", "agent": "jarvis", "text": "Usuario pidió conectar Meta", "payload": { "chat_id": "…" } }
   ```
3. **`POST /v1/webhooks/inbound/telegram`** sigue siendo alias válido de `…/inbound/telegram`.
4. El adapter ejecuta `activity-log event` con `--task jmc-channel-<channel>` y `--kind <channel>_in|_out`. Las líneas aparecen en **Activity** / resúmenes que lean `state/activity-log.jsonl` (alinear `JMC_STATE_DIR` / `JARVIS_STATE_DIR` con el mismo directorio `state/`).

**Nota v1.8 — efecto en agentes:** el adapter aplica el modo en **su** `os.environ` al instante; los procesos de agentes que lean `JARVIS_AUTONOMY_MODE` **solo al arrancar** verán el valor nuevo tras **reiniciar** esos agentes (o el shell donde corran). El `.env` queda alineado para el próximo arranque de OpenClaw/JARVIS.

### Chat con Jarvis (buzón `state/jmc-inbox/`)

- **Qué es:** cola **asíncrona** en disco: el CEO escribe desde la vista **Chat** de JMC (o vía API); Jarvis (Cursor/CLI) lee los `msg-*.json` y adjuntos, y deja `msg-*.reply.json`. La UI hace **polling** (~8 s). **No** es un cliente LLM ni chat en tiempo real: la latencia depende de cuándo Jarvis procese el buzón.
- **Dónde:** por defecto `state/jmc-inbox/` bajo la raíz del repo (o `JMC_CHAT_INBOX_DIR`). Conversaciones archivadas en `state/jmc-inbox/_archived/`.
- **Activity log:** cada `POST …/messages` registra `kind: jmc_inbox` con `--task jmc-chat-<conv_id>` (mismo patrón que canales inbound). Contrato JSON detallado: **[JMC_CHAT_INBOX.md](JMC_CHAT_INBOX.md)**.
- **Espejo opcional:** si `JMC_CHAT_MIRROR_ENABLED=1` y el usuario marca espejo en la UI, el adapter intenta `openclaw message send --channel telegram|discord --text "…"`. Los adjuntos **no** se envían por el canal; solo un resumen en texto. Si `openclaw` no está en el host, el guardado en disco sigue siendo 200 y `meta.warnings` incluye `openclaw_bin_missing`.
- **curl (mensaje solo texto):**
  ```bash
  export TOKEN='…'   # JMC_BEARER_TOKEN (≥32)
  export CID='conv-YYYY-MM-DD-xxxxxx'   # crear antes con POST /v1/chat/conversations
  curl -sS -H "Authorization: Bearer $TOKEN" \
    -F 'text=Hola Jarvis' \
    "http://127.0.0.1:8765/v1/chat/conversations/$CID/messages"
  ```

---

## Arrancar (manual)

```bash
export JMC_BEARER_TOKEN="$(openssl rand -hex 32)"
cd jarvis-ecosystem
. .venv-jmc/bin/activate
cd jmc/adapter
uvicorn app.main:app --host 127.0.0.1 --port 8765 --workers 1
```

UI: `http://127.0.0.1:8765/ui/` (configurar mismo token en header desde fetch si la UI lo requiere).

Con **Authorization:** `Bearer <token>` en cada petición API.

**URL base del API (UI v1.8+):** en **Conexión** puedes indicar un origen distinto al de la pestaña (p. ej. `http://127.0.0.1:8765` si abres la UI desde otro sitio). Se guarda en `localStorage` como `jmc_api_base`; vacío = peticiones al mismo host que la página (`fetch` relativo).

### Conexión rechazada en el puerto 8765 (`ERR_CONNECTION_REFUSED`)

Significa que **no hay ningún proceso escuchando** en esa IP y puerto (no es un fallo de la UI en sí).

1. Comprueba el puerto: `ss -lntp | grep 8765` (o `curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8765/ui/` → debe ser `200`, no error de conexión).
2. Si usas systemd: `systemctl status jmc-adapter` (system) o `systemctl --user status jmc-adapter` (usuario). Logs: `journalctl -u jmc-adapter -n 40` o `journalctl --user -u jmc-adapter -n 40`.
3. **`127.0.0.1` es solo la máquina local** donde corre uvicorn. Si el navegador está en otro PC o móvil, esa URL no llegará al adapter salvo túnel (SSH, VPN) o cambies `JMC_BIND` (expón solo en red de confianza; el default loopback es intencional por seguridad).

Tras instalar o actualizar el venv, vuelve a ejecutar `scripts/jmc-systemd-install.sh` para regenerar la unidad con la ruta correcta a `uvicorn`, o define `JMC_UVICORN_BIN` en el fichero de entorno del servicio.

---

## Arranque automático al reiniciar el equipo (recomendado)

Objetivo: **no** tener que ejecutar `jmc-start.sh` ni `uvicorn` tras cada reinicio de la PC.

**Qué obtienes:** instalas el servicio **una sola vez** (`jmc-systemd-install.sh`). A partir de ahí, **systemd arranca JMC al encender el equipo** (`systemctl enable` + `WantedBy=multi-user.target` en modo system). Si el proceso cae, la unidad lo **vuelve a levantar** (`Restart=always`). No hace falta abrir terminal ni “levantar servicios” en cada boot; solo comprueba `systemctl status jmc-adapter` si algo falla.

### Opción A — Servicio **system** (recomendado en servidor o equipo fijo)

1. Instalar el adapter en el venv (una vez):

   ```bash
   cd jarvis-ecosystem && python3 -m venv .venv-jmc && .venv-jmc/bin/pip install -e jmc/adapter
   ```

2. Instalar y habilitar systemd (genera `/etc/jmc/jmc-adapter.env` con token si no existe):

   ```bash
   cd jarvis-ecosystem
   sudo ./scripts/jmc-systemd-install.sh
   ```

   El script localiza `uvicorn` en este orden: variable `JMC_UVICORN_BIN` al invocar el script, línea `JMC_UVICORN_BIN=` en el fichero de entorno (si ya existe), `.venv-jmc/bin/uvicorn`, `venv/bin/uvicorn`, `$VIRTUAL_ENV/bin/uvicorn`, o el primer `uvicorn` en `PATH` (con aviso). La unidad usa `Restart=always` con límites de ráfaga para recuperarse de caídas.

   La unidad queda en `/etc/systemd/system/jmc-adapter.service`, corre como tu usuario (`SUDO_USER`), y arranca en **multi-user.target** (al iniciar Linux).

3. Ver estado y logs:

   ```bash
   systemctl status jmc-adapter
   journalctl -u jmc-adapter -f
   ```

4. Ver el token para la UI (solo lectura root):

   ```bash
   sudo grep JMC_BEARER_TOKEN /etc/jmc/jmc-adapter.env
   ```

   Guárdalo en un gestor de contraseñas; la página `/ui/` lo pide una vez (localStorage).

Archivo de ejemplo de variables: [`jmc/adapter/deploy/jmc-adapter.env.example`](../jmc/adapter/deploy/jmc-adapter.env.example).

### Opción B — Servicio **usuario** (`systemctl --user`)

Sin sudo en `/etc`; útil en escritorio Linux:

```bash
cd jarvis-ecosystem
./scripts/jmc-systemd-install.sh --user
```

Para que el servicio **usuario** arranque al reiniciar **aunque no hayas abierto sesión gráfica**, activa linger una vez:

```bash
loginctl enable-linger "$USER"
```

Sin linger, el servicio user solo sube cuando inicias sesión.

Con **linger** activado, el comportamiento es análogo al modo system respecto al reinicio: **JMC sube al arrancar la máquina** sin que tú ejecutes nada a mano.

---

## systemd (referencia manual)

La forma automatizada es `scripts/jmc-systemd-install.sh`. Si prefieres crear la unidad a mano, Inspírate en las opciones A/B arriba y usa `EnvironmentFile=` apuntando a un fichero con `JMC_BEARER_TOKEN`, `JMC_REPO_ROOT`, etc.

---

## PM2 (alternativa)

```bash
pm2 start "$(which uvicorn)" --name jmc-adapter --interpreter none \
  --cwd jarvis-ecosystem/jmc/adapter \
  -- app.main:app --host 127.0.0.1 --port 8765 --workers 1
```

Exportar `JMC_*` en el entorno del proceso PM2 o `ecosystem.config.js`.

---

## Reverse proxy

Solo si se expone fuera de localhost: **HTTPS + MFA delante** (patrón tipo tugcantopaloglu). El adapter v1 sigue escuchando `127.0.0.1`; el proxy termina TLS.

---

## Convenciones y alcance (v1.11)

### JMC como panel de lectura

- **Gates (AG-01…)** y **modos A/B/C/D**: el adapter **parsea** tablas y documentación para la UI; **no** bloquea acciones ni ejecuta políticas. El **enforcement** (qué puede hacer un agente) vive en el propio agente (p. ej. Jarvis leyendo `MEMORY.md` y skills), no en JMC.
- **Escalaciones**: ver `docs/ESCALACION_ASYNC.md` y la sección *Jarvis Mission Control* allí: `GET /v1/escalations` lista tareas `waiting_for_user` / `blocked`, no un CRUD de ficheros `state/escalations/*.json` hasta que exista ese diseño.

### Naming JSON (canon API)

Contrato recomendado para clientes e integraciones (migración gradual de respuestas que aún usan `id` en heartbeats):

| Campo | Uso |
|-------|-----|
| `agent_id` | Identificador de agente en APIs nuevas (`/v1/skills/coverage`, etc.). |
| `task_id` | Identificador de tarea (aceptar `taskId` solo como compatibilidad en parsers). |
| `dossier_id` | Identificador de dossier cliente (`cli-…`). |

Las respuestas históricas (`/v1/openclaw/agents` con `id`) se mantienen; alinear todo a este canon es objetivo de revisión **v1.11+**.

### Agentes en disco vs `agents.list`

En el repo existen carpetas bajo `agents/` (p. ej. **legal**, **contadores**, **dev-agency**) que pueden no aparecer en `agents.list` de `~/.openclaw/openclaw.json`. Si no están listados, **no** tendrán fila en vistas que lean solo OpenClaw (Heartbeats, Gateway, jerarquía); su actividad puede verse igual en **Activity** si el campo `agent` del JSONL coincide. Decide operativamente si son agentes de primera clase (añádelos a `agents.list` fuera del repo) o **grupos documentales** sin heartbeat en JMC.

### API pública no usada por la UI

Los siguientes endpoints están implementados y autenticados con Bearer pero **la UI estática actual no los consume**; sirven para integraciones, diagnósticos o futuras vistas:

- `GET /v1/costs/by-agent`
- `GET /v1/judge/last`
- `GET /v1/system/cpu-detail`, `GET /v1/system/proc-summary`, `GET /v1/system/fs-latency`
- `GET /v1/runtime/services` (y journal opcional)
- `GET /v1/external/healthchecks`
- `POST /v1/webhooks/test`, `POST /v1/webhooks/notify`
- `POST /v1/csp-report`

No se consideran “muertos”: están expuestos de forma deliberada; si se eliminan en el futuro, conviene changelog y semver.

---

## Troubleshooting

| Síntoma | Causa probable | Acción |
|---------|----------------|--------|
| **«Sin API»** en la UI (cabecera roja) | `/v1/health` devuelve 401: el adapter **exige Bearer** también para health. Token del navegador distinto al de `JMC_BEARER_TOKEN`, o URL base del API mal (otro puerto). | En **Conexión**: pegar el token de `sudo grep JMC_BEARER_TOKEN /etc/jmc/jmc-adapter.env` (o el de su `EnvironmentFile`). Dejar **URL base del API** vacía si abre `/ui/` en el mismo host/puerto que uvicorn (p. ej. `http://127.0.0.1:8765/ui/` → API en `8765`, no `8785`). Guardar y esperar **API OK**. |
| `401` | Token ausente o incorrecto | Exportar `JMC_BEARER_TOKEN` y enviar header `Authorization`. |
| `503` al arrancar | Token &lt; 32 chars | Regenerar token. |
| Puerto ocupado | Otro proceso | Cambiar `JMC_PORT` o liberar puerto. |
| Costes vacíos | Sin sesiones en mes | Verificar `OPENCLAW_HOME` y `scripts/cost-report.sh` manualmente. |
| Paths con espacios | Shell | Comillas en `WorkingDirectory` y rutas. |
| `cost-report.sh` lento | Muchos JSONL | Normal; el adapter cachea ~60s. |

**Comprobar modos (con token real):**

```bash
TOKEN="$(sudo grep -oP '(?<=^JMC_BEARER_TOKEN=).*' /etc/jmc/jmc-adapter.env)"
curl -sS -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8765/v1/modes/current | python3 -c "import sys,json; d=json.load(sys.stdin); print('mode_write_enabled=', d['data'].get('mode_write_enabled'))"
```

### Checklist tras F5 (persistencia y Aplicar)

1. **Conexión** → pegar el mismo Bearer que `JMC_BEARER_TOKEN` del servicio → **Guardar**. Sin **Guardar**, el token no se guarda en el navegador y al recargar verá **Sin API**.
2. **Aplicar** en Modes funciona con Bearer guardado; la API devuelve `mode_write_enabled=true` siempre (el `curl` de arriba debe mostrar `True`).
3. El intervalo de **Polling (s)** se persiste en el navegador al cambiar el valor o al pulsar **Guardar** (clave localStorage `jmc_poll_sec`).

---

## Smoke

```bash
./scripts/jmc-smoke.sh
```
