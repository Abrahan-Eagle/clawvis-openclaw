# Runbook forense: OpenClaw + Jarvis

Documento operativo para baseline, integridad de sesiones, límites LLM, secretos y comprobaciones periódicas. La configuración viva no se versiona; rutas de ejemplo asumen usuario `aipp`.

## Fase A — Baseline y trazabilidad

1. **Estado del runtime**
   - `openclaw doctor` — revisar integridad de sesiones, `gateway.auth`, PATH/Node, WhatsApp policies.
   - `openclaw channels status --probe` — Telegram/Discord OK; WhatsApp según enlace.

2. **Logs**
   - Directorio típico: `/tmp/openclaw/openclaw-*.log` (rotación por fecha).
   - Para correlacionar un incidente: anotar **timestamp UTC** del mensaje en Telegram y buscar en el log del día cadenas como `diagnostic`, `agent/embedded`, `model-fallback`, `gateway/channels/telegram`.

3. **Inventario rápido de sesiones**
   - `openclaw sessions cleanup --store "$HOME/.openclaw/agents/jarvis/sessions/sessions.json" --dry-run`
   - Revisar salida: entradas huérfanas, transcripts faltantes (el doctor puede advertir “missing transcripts”).

## Fase B — Integridad `sessions.json` ↔ `*.jsonl`

### Síntomas

- Error genérico en Telegram tras `/start` o mensaje de texto.
- `openclaw doctor` reporta sesiones recientes sin transcript coherente.

### Comprobaciones

1. Cada clave en `sessions.json` con `sessionFile` debe apuntar a un **fichero existente** en disco.
2. Para el mismo peer de Telegram, **`telegram:direct`** y **`telegram:slash`** deben usar el **mismo** `sessionId` y `sessionFile` (o ambos regenerados de forma coordinada), salvo decisión explícita documentada de mantener historiales separados.
3. **Primera línea** del `.jsonl` activo (tipo `session`): `cwd` debe coincidir con el `workspace` del agente en `agents.list` (p. ej. `jarvis` → ruta bajo `jarvis-ecosystem/agents/jarvis`).

### Automatización

- Script en el repo: `jarvis-ecosystem/agents/jarvis/scripts/validate-jarvis-sessions.mjs` (ver sección al final).
- Tras editar `sessions.json` manualmente: **reiniciar** el gateway (`systemctl --user restart openclaw-gateway` o el unit que uses) para evitar estado en memoria desalineado.

### Limpieza asistida

- `openclaw sessions cleanup --store <ruta/sessions.json> --dry-run` primero; si el resultado es aceptable, valorar `--enforce` según documentación de tu versión de OpenClaw.

## Fase C — `contextTokens` y límites Groq (TPM)

1. **Mínimo OpenClaw**  
   - `agents.defaults.contextTokens` debe ser **≥ 16000**. Valores menores hacen fallar el agente embebido con mensaje tipo *Minimum is 16000* antes de resolver cuotas del proveedor.
   - Configuración verificada en esta instalación: **16384** en `~/.openclaw/openclaw.json` (no bajar por “ahorro” sin validar el runtime).

2. **Timeout en OpenCode (`opencode:zen*` / perfil primero)**  
   - En el log puede aparecer `Profile opencode:zen1 timed out` tras ~60s: la llamada al API OpenCode no respondió a tiempo; el usuario ve el error genérico de Telegram mientras el failover rota perfiles.  
   - **Mitigación:** usar **`openrouter/free` (u otro proveedor rápido) como `primary`** y dejar OpenCode en `fallbacks`, o revisar red/firewall y validez de claves OpenCode.

3. **413 / TPM en Groq (tier gratuito)**  
   - No se soluciona reduciendo `contextTokens` por debajo del mínimo.
   - **Síntoma verificado en logs/transcript:** `413 Request too large ... on tokens per minute (TPM)` con *Requested* ~40k+ y *Limit* 6000–12000 según modelo — el **prompt completo** (system + tools + skills + bootstrap) supera el cupo **TPM** del tier gratuito de Groq, no solo “context window”.
   - **Mitigación efectiva:** poner **`primary` en un proveedor que aguante el payload** (p. ej. `opencode/nemotron-3-super-free` o `openrouter/free`) y dejar **Groq en `fallbacks`** para cuando el proveedor principal falle por otra causa; o subir tier en Groq (Dev/Billing).
   - Otras palancas: menos skills visibles, `bootstrapTotalMaxChars` / `bootstrapMaxChars` más bajos, compaction más agresiva (`reserveTokens` / `keepRecentTokens`), **auth-profiles** válidos para OpenCode/OpenRouter.

4. **Bootstrap demasiado recortado**  
   - Si `agents.defaults.bootstrapTotalMaxChars` es muy bajo (p. ej. 12000 frente al default documentado ~150000), `BOOTSTRAP.md` y otros archivos pueden quedar casi vacíos en el prompt y aparecer avisos de truncado agresivo por archivo. Subir `bootstrapTotalMaxChars` y fijar `bootstrapMaxChars` (p. ej. 20000) según la referencia de OpenClaw.

5. **Error `EACCES: mkdir '/home/will'` (ruta legada)**  
   - Suele aparecer si algo en el estado o en `cwd` de sesión apunta a un home antiguo; unificar `cwd` del `.jsonl` con el `workspace` del agente y buscar `/home/will` en transcripts activos.

6. **Revisión tras cambios**  
   - Vuelve a probar un mensaje corto y revisa en log líneas `model-fallback` / decisión de proveedor.

## Fase D — Secretos y gateway

1. **No versionar** `openclaw.json` ni `.env` con secretos en repos públicos. Tokens de Telegram, Discord, etc. deben vivir en variables de entorno o ficheros ignorados por git donde el proyecto lo permita.

2. **Rotación**  
   - Si un token se expuso (chat, captura, commit): revocar en el proveedor (BotFather, Discord Developer Portal, etc.), generar nuevo valor y actualizar solo el almacenamiento local/seguro.

3. **`gateway.auth`**  
   - `none` en loopback puede ser aceptable si el puerto no es alcanzable desde la red; si el gateway escucha en interfaz no local o hay riesgo de acceso lateral, documentar endurecimiento (token, bind a `127.0.0.1`, firewall).

## Fase E — Rutas legadas y checklist periódico

1. **Migración de usuario (`/home/will`, etc.)**  
   - Transcripts **archivados** (p. ej. `*.jsonl.reset.*`) pueden contener `cwd` o mensajes con rutas antiguas; es histórico.  
   - Los **`.jsonl` activos** referenciados por `sessions.json` no deberían usar rutas de otro usuario; si aparecen, corregir `cwd` en la cabecera de sesión o regenerar sesión tras backup.

2. **Búsqueda sugerida (semanal o tras incidente)**

   ```bash
   rg '/home/will' ~/.openclaw/agents/jarvis/sessions --glob '*.jsonl' --glob '!*.reset.*'
   ```

   Si hay coincidencias en archivos activos, revisar y alinear con el workspace actual.

3. **Actualizaciones de OpenClaw**  
   - Releer notas de versión por cambios en mínimos de `contextTokens` o formato de sesión.

## Script: `validate-jarvis-sessions.mjs`

Ubicación: `jarvis-ecosystem/agents/jarvis/scripts/validate-jarvis-sessions.mjs`.

```bash
cd jarvis-ecosystem/agents/jarvis/scripts
node validate-jarvis-sessions.mjs
# Opcional: comprobar prefijo de cwd en la primera línea del jsonl
EXPECTED_WORKSPACE="/home/aipp/jarvis-ecosystem/agents/jarvis" node validate-jarvis-sessions.mjs
# Fallar si cwd no coincide con el prefijo esperado
VALIDATE_STRICT_CWD=1 EXPECTED_WORKSPACE="/home/aipp/jarvis-ecosystem/agents/jarvis" node validate-jarvis-sessions.mjs
```

Variables:

| Variable | Descripción |
|----------|-------------|
| `SESSIONS_STORE` | Ruta a `sessions.json` (por defecto `~/.openclaw/agents/jarvis/sessions/sessions.json`) |
| `EXPECTED_WORKSPACE` | Si está definida, se compara el `cwd` de la primera línea de cada transcript con este prefijo |
| `VALIDATE_STRICT_CWD` | Si es `1`, distinto prefijo → código de salida distinto de cero |

Códigos de salida: `0` OK; `1` falta algún `sessionFile`; `2` no existe el store; `3` advertencia estricta de `cwd` (solo con `VALIDATE_STRICT_CWD=1`).

---

**Última revisión:** forense multi-rol OpenClaw + Jarvis (sesiones Telegram unificadas, `contextTokens` 16384, validación automatizada).
