# Spike: Cursor LLM + OpenClaw (abril 2026)

Registro de pruebas en **Linux** para el plan *Análisis Cursor–OpenClaw*. No incluye secretos ni volcados de `openclaw.json`.

---

## Entorno de referencia

| Componente | Valor observado |
|------------|-----------------|
| OS | Linux x64 |
| Node | v22.x (nvm) |
| OpenClaw | 2026.4.2 (`openclaw --version`) |
| Cursor Agent CLI | instalado vía `curl -fsSL https://cursor.com/install \| bash` → `~/.local/bin/agent` |

**PATH:** el proxy npm busca el binario `agent`; conviene `export PATH="$HOME/.local/bin:$PATH"` en shells/servicios que arranquen el proxy.

---

## Autenticación Cursor (solo tú puedes cerrarla)

El CLI responde **`Not logged in`** hasta que completes una de estas vías:

1. **Login interactivo** (recomendado en escritorio): en una terminal **con navegador** disponible:

   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   agent login
   ```

   Si no quieres que abra el navegador automáticamente: `NO_OPEN_BROWSER=1 agent login` y sigue la URL o el flujo que imprima.

2. **API key** (adecuado para headless): clave en [cursor.com/settings](https://cursor.com/settings) → variable de entorno **`CURSOR_API_KEY`**. Para el **gateway systemd**, suele ir en `~/.openclaw/.env` (ya referenciado por `EnvironmentFile=-%h/.openclaw/.env` en la unidad de usuario), **sin commitear** ese archivo:

   ```bash
   echo 'CURSOR_API_KEY=tu_clave_aqui' >> ~/.openclaw/.env
   systemctl --user restart openclaw-gateway.service
   ```

Después de autenticar:

```bash
agent status
agent models    # o: agent --list-models
openclaw cursor-brain setup   # TTY interactivo; elige modelos si los lista
```

Sin sesión válida, **`openclaw-cursor-brain` seguirá con “0 models”** aunque el proxy y el gateway estén bien.

---

## Gateway systemd y `PATH` (Linux)

La unidad `~/.config/systemd/user/openclaw-gateway.service` generada por OpenClaw suele tener un `PATH` **mínimo** sin `~/.local/bin`. El gateway entonces no encuentra `agent` al arrancar el plugin. **Corrección aplicada en el host de referencia:** anteponer `/home/aipp/.local/bin` al `Environment=PATH=...` de la unidad, luego:

```bash
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway.service
```

Sustituye el usuario si no es `aipp`.

---

## Línea A — `cursor-agent-api-proxy`

1. **Instalación npm global**

   `npm install -g cursor-agent-api-proxy`

   Binario: `cursor-agent-api` (puerto por defecto **4646**).

2. **Sin CLI Cursor:** al ejecutar `cursor-agent-api run 4646`, el proceso **no** levanta el listener y el log indica instalar el CLI y `agent login`.

3. **Con CLI instalado:** `GET http://127.0.0.1:4646/health` respondió JSON de estado OK, con `cli_version` y `provider: "cursor-agent-api-proxy"`.

4. **Coexistencia de puertos:** con Gateway OpenClaw en **18789**, el proxy en **4646** no chocó.

---

## Línea B — `openclaw-cursor-brain`

1. **Instalación:** `openclaw plugins install openclaw-cursor-brain` fue **bloqueada** por el escáner de código “peligroso” (uso de `child_process`, etc.). Instalación forzada con:

   `openclaw plugins install openclaw-cursor-brain --dangerously-force-unsafe-install`

2. **Post-instalación:** el instalador sugirió `openclaw gateway restart` y opcionalmente `openclaw cursor-brain setup` para modelos primary/fallback.

3. **`openclaw cursor-brain doctor`:** la mayoría de chequeos en verde (CLI, MCP file, `mcp.json`, proveedor `cursor-local` en `http://127.0.0.1:18790/v1`). Fallos observados en un run concreto: “No tools found” (plugins/canal) y “Gateway REST API unreachable” (posible ventana de tiempo o proxy que se mató durante el doctor). Tras el doctor, el **streaming proxy** quedó escuchando en **18790** sin colisión con **18789** ni **4646**.

4. **Descubrimiento de modelos:** el plugin reportó **0 modelos** parseados tras `agent --list-models` (tres reintentos). Es coherente con **sesión no autenticada** o salida del CLI distinta a la esperada; siguiente paso operativo: `agent login` o `CURSOR_API_KEY` y repetir `doctor` / `setup`.

5. **`plugins.allow`:** Si el array **tiene elementos**, solo esos IDs de plugin pueden cargarse: hay que incluir explícitamente los canales que uses (`telegram`, `discord`, `whatsapp`, …) además de otros como `browser`. Si falta un canal en la lista, puede quedar desactivado aunque `channels.<id>.enabled` sea `true`. Ver respaldo detallado en [`RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md`](RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md).

---

## Decisión: proxy npm (4646) sobre cursor-brain (18790)

En abril 2026, en el host de referencia (Linux, OpenClaw 2026.4.2, cursor-brain 1.5.4) el plugin **cursor-brain generaba un bucle de reinicio** del gateway: el plugin escribe la lista de 83 modelos en `openclaw.json`, el gateway detecta cambios, se auto-reinicia (SIGUSR1), el proxy hijo en 18790 muere (SIGKILL) antes de poder atender peticiones, y repite. Puerto 18790 nunca queda estable.

El proxy npm (`cursor-agent-api-proxy`) en **4646** no tiene ese problema: corre como servicio systemd independiente, no reescribe `openclaw.json` y no depende del ciclo de vida del gateway.

**Validación:** `curl http://127.0.0.1:4646/v1/chat/completions` con `model: composer-2-fast` devolvió respuesta correcta. `openclaw agent --agent jarvis` respondió usando `provider: cursor-local`, `model: composer-2-fast` sin caer a fallback.

**Config aplicada:** `baseUrl` = `http://127.0.0.1:4646/v1`, plugin cursor-brain `enabled: false`, servicio `cursor-agent-api.service` (systemd user, auto-start).

---

## Matriz de puertos (elección documentada)

| Servicio | Puerto | Estado |
|----------|--------|--------|
| OpenClaw Gateway | **18789** | Activo (loopback) |
| Proxy `cursor-agent-api-proxy` | **4646** | Activo (recomendado) |
| Proxy `openclaw-cursor-brain` | **18790** | Deshabilitado (bucle de reinicio) |

---

## Integración OpenClaw (recordatorio)

- Patrón: proveedor **OpenAI-compatible** (`api: "openai-completions"`, `baseUrl` al `/v1` del proxy elegido).
- Doc upstream del proxy npm: PR [openclaw/openclaw#42731](https://github.com/openclaw/openclaw/pull/42731) (verificar en GitHub si ya mergeado).
- **ToS Cursor:** las llamadas siguen siendo contra la nube de Cursor a través del CLI.

---

## Referencias en este repo

- [`RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md`](RESPALDO_OPENCLAW_CONFIGURACION_APLICADA.md) — respaldo de lo aplicado en el host (systemd, `openclaw.json` relevante, `plugins.allow`, sin secretos).
- [`PROVEEDOR_CURSOR_OPENCLAW.md`](PROVEEDOR_CURSOR_OPENCLAW.md) — guía y enlaces.
- [`MODELOS_JARVIS_OPENCLAW.md`](MODELOS_JARVIS_OPENCLAW.md) — sección “Proveedor Cursor”.
